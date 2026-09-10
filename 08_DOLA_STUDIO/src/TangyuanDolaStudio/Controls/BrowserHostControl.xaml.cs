using System.IO;
using System.Windows;
using System.Windows.Controls;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;
using TangyuanDolaStudio.Services;

namespace TangyuanDolaStudio.Controls;

public partial class BrowserHostControl : UserControl
{
    private WebView2? _webView;
    private string? _downloadFolder;

    public event EventHandler<string>? StatusChanged;
    public event EventHandler<string>? AddressChanged;
    public event EventHandler<bool>? RunningChanged;

    public bool IsRunning => _webView?.CoreWebView2 is not null;
    public bool CanGoBack => _webView?.CoreWebView2?.CanGoBack == true;
    public bool CanGoForward => _webView?.CoreWebView2?.CanGoForward == true;

    public BrowserHostControl()
    {
        InitializeComponent();
    }

    public async Task OpenAsync(CoreWebView2Environment environment, string homeUrl, string downloadFolder)
    {
        Close();
        _downloadFolder = downloadFolder;
        Directory.CreateDirectory(downloadFolder);

        var webView = new WebView2
        {
            HorizontalAlignment = HorizontalAlignment.Stretch,
            VerticalAlignment = VerticalAlignment.Stretch
        };

        _webView = webView;

        // Important: put the control in the WPF visual tree before explicit WebView2 initialization.
        // The reference app also isolates browser lifetime behind a BrowserHost component.
        RootGrid.Children.Clear();
        RootGrid.Children.Add(webView);

        webView.CoreWebView2InitializationCompleted += WebView_CoreWebView2InitializationCompleted;
        StatusChanged?.Invoke(this, "正在初始化 WebView2...");
        AppLogger.Info($"BrowserHost initialize; UDF={environment.UserDataFolder}; home={homeUrl}");

        try
        {
            await webView.EnsureCoreWebView2Async(environment);

            if (webView.CoreWebView2 is null)
                throw new InvalidOperationException("WebView2 初始化完成但 CoreWebView2 为空。\n");

            ConfigureCore(webView.CoreWebView2);
            RunningChanged?.Invoke(this, true);

            var target = NormalizeDolaUrl(homeUrl);
            StatusChanged?.Invoke(this, $"正在打开 Dola：{target}");
            webView.CoreWebView2.Navigate(target);
        }
        catch
        {
            Close();
            throw;
        }
    }

    private void ConfigureCore(CoreWebView2 core)
    {
        core.Settings.AreDevToolsEnabled = true;
        core.Settings.AreDefaultContextMenusEnabled = true;
        core.Settings.IsStatusBarEnabled = true;
        core.Settings.IsZoomControlEnabled = true;

        core.NavigationStarting += Core_NavigationStarting;
        core.NavigationCompleted += Core_NavigationCompleted;
        core.SourceChanged += Core_SourceChanged;
        core.ProcessFailed += Core_ProcessFailed;
        core.DownloadStarting += Core_DownloadStarting;
        core.NewWindowRequested += Core_NewWindowRequested;
    }

    private static string NormalizeDolaUrl(string? homeUrl)
    {
        var value = string.IsNullOrWhiteSpace(homeUrl) ? "https://www.dola.com/chat/" : homeUrl.Trim();
        if (value.Equals("https://www.dola.com/", StringComparison.OrdinalIgnoreCase) ||
            value.Equals("https://dola.com/", StringComparison.OrdinalIgnoreCase))
        {
            return "https://www.dola.com/chat/";
        }

        return value;
    }

    public void Navigate(string url)
    {
        var core = _webView?.CoreWebView2;
        if (core is null)
            throw new InvalidOperationException("浏览器尚未启动。请先打开账号实例。");

        var value = (url ?? string.Empty).Trim();
        if (!value.StartsWith("http://", StringComparison.OrdinalIgnoreCase) &&
            !value.StartsWith("https://", StringComparison.OrdinalIgnoreCase))
        {
            value = "https://" + value;
        }

        if (!Uri.TryCreate(value, UriKind.Absolute, out var uri))
            throw new UriFormatException("地址格式无效。");

        core.Navigate(uri.ToString());
    }

    public void GoBack()
    {
        if (CanGoBack)
            _webView!.CoreWebView2.GoBack();
    }

    public void GoForward()
    {
        if (CanGoForward)
            _webView!.CoreWebView2.GoForward();
    }

    public void Reload() => _webView?.CoreWebView2?.Reload();

    public void Close()
    {
        var webView = _webView;
        _webView = null;

        if (webView is not null)
        {
            try
            {
                if (webView.CoreWebView2 is { } core)
                {
                    core.NavigationStarting -= Core_NavigationStarting;
                    core.NavigationCompleted -= Core_NavigationCompleted;
                    core.SourceChanged -= Core_SourceChanged;
                    core.ProcessFailed -= Core_ProcessFailed;
                    core.DownloadStarting -= Core_DownloadStarting;
                    core.NewWindowRequested -= Core_NewWindowRequested;
                }

                webView.CoreWebView2InitializationCompleted -= WebView_CoreWebView2InitializationCompleted;
                webView.Dispose();
            }
            catch (Exception ex)
            {
                AppLogger.Warn($"BrowserHost dispose warning: {ex.Message}");
            }
        }

        RootGrid.Children.Clear();
        RootGrid.Children.Add(Placeholder);
        RunningChanged?.Invoke(this, false);
    }

    private void WebView_CoreWebView2InitializationCompleted(object? sender, CoreWebView2InitializationCompletedEventArgs e)
    {
        if (e.IsSuccess)
        {
            AppLogger.Info("WebView2 initialization completed successfully.");
            return;
        }

        var message = e.InitializationException?.Message ?? "Unknown WebView2 initialization error";
        AppLogger.Error("WebView2 initialization failed.", e.InitializationException);
        StatusChanged?.Invoke(this, $"WebView2 初始化失败：{message}");
    }

    private void Core_NavigationStarting(object? sender, CoreWebView2NavigationStartingEventArgs e)
    {
        AppLogger.Info($"NavigationStarting: {e.Uri}");
        StatusChanged?.Invoke(this, $"加载：{e.Uri}");
    }

    private void Core_NavigationCompleted(object? sender, CoreWebView2NavigationCompletedEventArgs e)
    {
        if (e.IsSuccess)
        {
            var url = _webView?.Source?.ToString() ?? _webView?.CoreWebView2?.Source ?? string.Empty;
            AppLogger.Info($"NavigationCompleted: {url}");
            StatusChanged?.Invoke(this, $"Dola 页面已加载：{url}");
        }
        else
        {
            AppLogger.Warn($"Navigation failed: {e.WebErrorStatus}");
            StatusChanged?.Invoke(this, $"页面加载失败：{e.WebErrorStatus}");
        }
    }

    private void Core_SourceChanged(object? sender, CoreWebView2SourceChangedEventArgs e)
    {
        var address = _webView?.CoreWebView2?.Source;
        if (!string.IsNullOrWhiteSpace(address))
            AddressChanged?.Invoke(this, address);
    }

    private void Core_ProcessFailed(object? sender, CoreWebView2ProcessFailedEventArgs e)
    {
        AppLogger.Error($"WebView2 process failed: {e.ProcessFailedKind}");
        StatusChanged?.Invoke(this, $"WebView2 进程异常：{e.ProcessFailedKind}");
    }

    private void Core_DownloadStarting(object? sender, CoreWebView2DownloadStartingEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_downloadFolder))
            return;

        Directory.CreateDirectory(_downloadFolder);
        var suggestedName = Path.GetFileName(e.ResultFilePath);
        if (string.IsNullOrWhiteSpace(suggestedName))
            suggestedName = $"download-{DateTime.Now:yyyyMMdd-HHmmss}.bin";

        var target = MakeUniquePath(Path.Combine(_downloadFolder, suggestedName));
        e.ResultFilePath = target;
        AppLogger.Info($"DownloadStarting: {target}");
        StatusChanged?.Invoke(this, $"下载 → {target}");
    }

    private void Core_NewWindowRequested(object? sender, CoreWebView2NewWindowRequestedEventArgs e)
    {
        // Keep normal web navigation inside the same profile container instead of losing the user's session
        // to a separate unmanaged browser window. No token/cookie scraping is performed.
        if (Uri.TryCreate(e.Uri, UriKind.Absolute, out var uri) &&
            (uri.Scheme == Uri.UriSchemeHttps || uri.Scheme == Uri.UriSchemeHttp))
        {
            e.Handled = true;
            AppLogger.Info($"NewWindowRequested -> same profile navigation: {e.Uri}");
            _webView?.CoreWebView2?.Navigate(e.Uri);
        }
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
}
