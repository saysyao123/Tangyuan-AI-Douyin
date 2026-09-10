using System.Windows;
using System.Windows.Threading;
using TangyuanDolaStudio.Services;

namespace TangyuanDolaStudio;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        DispatcherUnhandledException += OnDispatcherUnhandledException;
        AppDomain.CurrentDomain.UnhandledException += OnDomainUnhandledException;
        TaskScheduler.UnobservedTaskException += OnUnobservedTaskException;

        try
        {
            var runtime = Microsoft.Web.WebView2.Core.CoreWebView2Environment.GetAvailableBrowserVersionString();
            AppLogger.Info($"Application startup. WebView2 Runtime={runtime}");
        }
        catch (Exception ex)
        {
            AppLogger.Error("Application startup; WebView2 Runtime detection failed.", ex);
        }

        base.OnStartup(e);
    }

    private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        AppLogger.Error("Unhandled UI exception", e.Exception);
        MessageBox.Show(
            $"程序遇到异常，但已拦截，避免直接闪退。\n\n{e.Exception.Message}\n\n日志：{AppLogger.LogFile}",
            "Tangyuan Dola Studio",
            MessageBoxButton.OK,
            MessageBoxImage.Error);
        e.Handled = true;
    }

    private static void OnDomainUnhandledException(object? sender, UnhandledExceptionEventArgs e)
    {
        AppLogger.Error("Unhandled AppDomain exception", e.ExceptionObject as Exception);
    }

    private static void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
    {
        AppLogger.Error("Unobserved task exception", e.Exception);
        e.SetObserved();
    }
}
