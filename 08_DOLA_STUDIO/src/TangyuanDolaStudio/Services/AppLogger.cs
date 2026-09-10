using System.IO;
using System.Text;

namespace TangyuanDolaStudio.Services;

public static class AppLogger
{
    private static readonly object Sync = new();

    public static string LogDirectory { get; } = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "TangyuanDolaStudio",
        "logs");

    public static string LogFile { get; } = Path.Combine(LogDirectory, "app.log");

    public static void Info(string message) => Write("INFO", message, null);
    public static void Warn(string message) => Write("WARN", message, null);
    public static void Error(string message, Exception? exception = null) => Write("ERROR", message, exception);

    private static void Write(string level, string message, Exception? exception)
    {
        try
        {
            Directory.CreateDirectory(LogDirectory);
            var sb = new StringBuilder();
            sb.Append(DateTimeOffset.Now.ToString("yyyy-MM-dd HH:mm:ss.fff zzz"));
            sb.Append(" [").Append(level).Append("] ").AppendLine(message);
            if (exception is not null)
                sb.AppendLine(exception.ToString());

            lock (Sync)
            {
                File.AppendAllText(LogFile, sb.ToString(), Encoding.UTF8);
            }
        }
        catch
        {
            // Logging must never crash the application.
        }
    }
}
