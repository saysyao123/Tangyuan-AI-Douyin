using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;
using Microsoft.VisualBasic;
using TangyuanDolaStudio.Models;
using TangyuanDolaStudio.Services;

namespace TangyuanDolaStudio;

public partial class MainWindow : Window
{
    private readonly ProfileStore _profileStore = new();
    private readonly BrowserInstanceManager _browserManager;
    private readonly ObservableCollection<ProfileItem> _profiles = new();

    private WebView2? _webView;
    private ProfileItem? _activeProfile;

    public MainWindow()
    {
        InitializeComponent();
        _browserManager = new BrowserInstanceManager(_profileStore);
        ProfilesList.ItemsSource = _profiles;
        Loaded += MainWindow_Loaded;
        Closing += MainWindow_Closing;
    }

    private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
    {
        try
        {
            var loaded = await _profileStore.LoadAsync();
            foreach (var profile in loaded)
                _profiles.Add(profile);

            if (_profiles.Count == 0)
            {
                _profiles.Add(NewProfile("Dola-001"));
                _profiles.Add(NewProfile("Dola-002"));
                await SaveProfilesAsync();
            }

            ProfilesList.SelectedIndex = 0;
            StatusText.Text = "P1 Ready：请选择账号并打开 Dola。首次使用请由你本人正常登录。";
        }
        catch (Exception ex)
        {
            MessageBox.Show($"初始化失败：\n{ex.Message}", "Tangyuan Dola Studio", MessageBoxButton.OK, MessageBoxImage.Error);
            StatusText.Text = "初始化失败";
        }
    }

    private void MainWindow_Closing(object? sender, CancelEventArgs e)
    {
        StopBrowserInternal();
    }

    private ProfileItem NewProfile(string displayName) => new()
    {
        Id = Guid.NewGuid().ToString("N"),
        DisplayName = displayName,
        HomeUrl = "https://www.dola.com/",
        CreatedAt = DateTimeOffset.Now
    };

    private async Task SaveProfilesAsync()
    {
        await _profileStore.SaveAsync(_profiles);
    }

    private ProfileItem? SelectedProfile => ProfilesList.SelectedItem as ProfileItem;

    private void ProfilesList_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        RefreshProfileDetails(SelectedProfile);
    }

    private async void AddProfile_Click(object sender, RoutedEventArgs e)
    {
        var defaultName = $"Dola-{_profiles.Count + 1:000}";
        var name = Interaction.InputBox("给这个 Dola 实例起一个名称：", "添加账号实例", defaultName).Trim();
        if (string.IsNullOrWhiteSpace(name))
            return;

        var profile = NewProfile(name);
        _profileStore.EnsureProfileFolders(profile);
        _profiles.Add(profile);
        await SaveProfilesAsync();
        ProfilesList.SelectedItem = profile;
        StatusText.Text = $"已创建 {profile.DisplayName}。每个实例都有独立的 WebView2 数据目录。";
    }

    private async void RenameProfile_Click(object sender, RoutedEventArgs e)
    {
        var profile = SelectedProfile;
        if (profile is null)
            return;

        var name = Interaction.InputBox("新的实例名称：", "重命名", profile.DisplayName).Trim();
        if (string.IsNullOrWhiteSpace(name) || name == profile.DisplayName)
            return;

        profile.DisplayName = name;
        await SaveProfilesAsync();
        ProfilesList.Items.Refresh();
        RefreshProfileDetails(profile);
        StatusText.Text = "实例已重命名。";
    }

    private async void DeleteProfile_Click(object sender, RoutedEventArgs e)
    {
        var profile = SelectedProfile;
        if (profile is null)
            return;

        var result = MessageBox.Show(
            $"删除实例“{profile.DisplayName}”？\n\n这会删除该实例的本地浏览器 Session 和下载目录。",
            "删除账号实例",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning);

        if (result != MessageBoxResult.Yes)
            return;

        if (_activeProfile?.Id == profile.Id)
            StopBrowserInternal();

        _browserManager.Forget(profile);
        _profiles.Remove(profile);
        await SaveProfilesAsync();

        try
        {
            _profileStore.DeleteProfileData(profile);
            StatusText.Text = $"已删除 {profile.DisplayName} 及其本地数据。";
        }
        catch (Exception ex)
        {
            StatusText.Text = $"已删除实例记录；部分浏览器文件仍被占用，可退出程序后手动清理。{ex.Message}";
        }

        ProfilesList.SelectedIndex = _profiles.Count > 0 ? 0 : -1;
    }

    private async void OpenProfile_Click(object sender, RoutedEventArgs e)
    {
        var profile = SelectedProfile;
        if (profile is null)
        {
            StatusText.Text = "请先选择一个账号实例。";
            return;
        }

        await OpenProfileAsync(profile);
    }

    private async Task OpenProfileAsync(ProfileItem profile)
    {
        StatusText.Text = $"正在启动 {profile.DisplayName} 的独立 WebView2 Session...";
        IsEnabled = false;

        try
        {
            StopBrowserInternal(showPlaceholder: false);

            var environment = await _browserManager.GetEnvironmentAsync(profile);
            var webView = new WebView2();
            await webView.EnsureCoreWebView2Async(environment);

            webView.CoreWebView2.Settings.AreDevToolsEnabled = true;
            webView.CoreWebView2.Settings.AreDefaultContextMenusEnabled = true;
            webView.CoreWebView2.Settings.IsStatusBarEnabled = true;

            webView.SourceChanged += WebView_SourceChanged;
            webView.NavigationStarting += WebView_NavigationStarting;
            webView.NavigationCompleted += WebView_NavigationCompleted;
            webView.CoreWebView2.ProcessFailed += CoreWebView2_ProcessFailed;
            webView.CoreWebView2.DownloadStarting += CoreWebView2_DownloadStarting;

            _webView = webView;
            _activeProfile = profile;
            profile.LastOpenedAt = DateTimeOffset.Now;
            await SaveProfilesAsync();

            BrowserHost.Children.Clear();
            BrowserHost.Children.Add(webView);

            TopProfileText.Text = $"{profile.DisplayName} · 独立 Session";
            SessionStateText.Text = "浏览器：运行中";
            RefreshProfileDetails(profile);

            webView.Source = new Uri(profile.HomeUrl);
            StatusText.Text = $"{profile.DisplayName} 已启动。首次请正常登录 Dola，之后 Session 会保存在该实例目录。";
        }
        catch (WebView2RuntimeNotFoundException)
        {
            ShowPlaceholder();
            MessageBox.Show(
                "未检测到 Microsoft Edge WebView2 Runtime。请安装或更新 WebView2 Runtime 后重试。",
                "缺少 WebView2 Runtime",
                MessageBoxButton.OK,
                MessageBoxImage.Warning);
            StatusText.Text = "WebView2 Runtime 不可用";
        }
        catch (Exception ex)
        {
            ShowPlaceholder();
            MessageBox.Show($"启动浏览器失败：\n{ex.Message}", "Tangyuan Dola Studio", MessageBoxButton.OK, MessageBoxImage.Error);
            StatusText.Text = "浏览器启动失败";
        }
        finally
        {
            IsEnabled = true;
        }
    }

    private void StopBrowser_Click(object sender, RoutedEventArgs e)
    {
        StopBrowserInternal();
        StatusText.Text = "当前浏览器已停止；Profile 数据仍保留在本地。";
    }

    private void StopBrowserInternal(bool showPlaceholder = true)
    {
        if (_webView is not null)
        {
            try
            {
                _webView.Dispose();
            }
            catch
            {
                // Best-effort cleanup during profile switches / shutdown.
            }
        }

        _webView = null;
        _activeProfile = null;
        BrowserHost.Children.Clear();

        if (showPlaceholder)
            BrowserHost.Children.Add(BrowserPlaceholder);

        TopProfileText.Text = "未打开账号";
        SessionStateText.Text = "浏览器：未启动";
    }

    private void ShowPlaceholder()
    {
        _webView = null;
        _activeProfile = null;
        BrowserHost.Children.Clear();
        BrowserHost.Children.Add(BrowserPlaceholder);
        TopProfileText.Text = "未打开账号";
        SessionStateText.Text = "浏览器：未启动";
    }

    private void RefreshProfileDetails(ProfileItem? profile)
    {
        if (profile is null)
        {
            ProfileNameText.Text = "未选择";
            ProfileIdText.Text = "-";
            return;
        }

        ProfileNameText.Text = profile.DisplayName;
        ProfileIdText.Text = $"ID: {profile.Id}\nUDF: {_profileStore.GetWebViewDataFolder(profile)}";
        SessionStateText.Text = _activeProfile?.Id == profile.Id ? "浏览器：运行中" : "浏览器：未启动";
    }

    private void WebView_SourceChanged(object? sender, CoreWebView2SourceChangedEventArgs e)
    {
        if (_webView?.Source is not null)
            AddressBox.Text = _webView.Source.ToString();
    }

    private void WebView_NavigationStarting(object? sender, CoreWebView2NavigationStartingEventArgs e)
    {
        StatusText.Text = $"加载：{e.Uri}";
    }

    private void WebView_NavigationCompleted(object? sender, CoreWebView2NavigationCompletedEventArgs e)
    {
        StatusText.Text = e.IsSuccess
            ? $"页面已加载 · {_activeProfile?.DisplayName}"
            : $"页面加载失败：{e.WebErrorStatus}";
    }

    private void CoreWebView2_ProcessFailed(object? sender, CoreWebView2ProcessFailedEventArgs e)
    {
        Dispatcher.Invoke(() => StatusText.Text = $"WebView2 进程异常：{e.ProcessFailedKind}");
    }

    private void CoreWebView2_DownloadStarting(object? sender, CoreWebView2DownloadStartingEventArgs e)
    {
        var profile = _activeProfile;
        if (profile is null)
            return;

        var downloads = _browserManager.GetDownloadsFolder(profile);
        var suggestedName = Path.GetFileName(e.ResultFilePath);
        if (string.IsNullOrWhiteSpace(suggestedName))
            suggestedName = $"download-{DateTime.Now:yyyyMMdd-HHmmss}.bin";

        var target = MakeUniquePath(Path.Combine(downloads, suggestedName));
        e.ResultFilePath = target;
        StatusText.Text = $"下载 → {target}";
    }

    private static string MakeUniquePath(string path)
    {
        if (!File.Exists(path))
            return path;

        var directory = Path.GetDirectoryName(path) ?? string.Empty;
        var name = Path.GetFileNameWithoutExtension(path);
        var extension = Path.GetExtension(path);

        for (var i = 1; i < 10000; i++)
        {
            var candidate = Path.Combine(directory, $"{name}-{i}{extension}");
            if (!File.Exists(candidate))
                return candidate;
        }

        return Path.Combine(directory, $"{name}-{Guid.NewGuid():N}{extension}");
    }

    private void Home_Click(object sender, RoutedEventArgs e)
    {
        NavigateTo(_activeProfile?.HomeUrl ?? SelectedProfile?.HomeUrl ?? "https://www.dola.com/");
    }

    private void Back_Click(object sender, RoutedEventArgs e)
    {
        if (_webView?.CoreWebView2?.CanGoBack == true)
            _webView.CoreWebView2.GoBack();
    }

    private void Forward_Click(object sender, RoutedEventArgs e)
    {
        if (_webView?.CoreWebView2?.CanGoForward == true)
            _webView.CoreWebView2.GoForward();
    }

    private void Refresh_Click(object sender, RoutedEventArgs e)
    {
        _webView?.CoreWebView2?.Reload();
    }

    private void Navigate_Click(object sender, RoutedEventArgs e)
    {
        NavigateTo(AddressBox.Text);
    }

    private void AddressBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter)
            NavigateTo(AddressBox.Text);
    }

    private void NavigateTo(string? input)
    {
        if (_webView?.CoreWebView2 is null)
        {
            StatusText.Text = "请先打开一个账号实例。";
            return;
        }

        var value = (input ?? string.Empty).Trim();
        if (string.IsNullOrWhiteSpace(value))
            return;

        if (!value.StartsWith("http://", StringComparison.OrdinalIgnoreCase) &&
            !value.StartsWith("https://", StringComparison.OrdinalIgnoreCase))
        {
            value = "https://" + value;
        }

        if (Uri.TryCreate(value, UriKind.Absolute, out var uri))
            _webView.CoreWebView2.Navigate(uri.ToString());
        else
            StatusText.Text = "地址格式无效。";
    }

    private void OpenDownloads_Click(object sender, RoutedEventArgs e)
    {
        var profile = _activeProfile ?? SelectedProfile;
        if (profile is null)
        {
            StatusText.Text = "请先选择账号实例。";
            return;
        }

        var folder = _browserManager.GetDownloadsFolder(profile);
        Process.Start(new ProcessStartInfo("explorer.exe", folder) { UseShellExecute = true });
    }
}
