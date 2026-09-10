using System.IO;
using System.Text.Json;
using TangyuanDolaStudio.Models;

namespace TangyuanDolaStudio.Services;

public sealed class ProfileStore
{
    private readonly JsonSerializerOptions _jsonOptions = new() { WriteIndented = true };
    private readonly SemaphoreSlim _ioLock = new(1, 1);

    public string AppRoot { get; } = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "TangyuanDolaStudio");

    public string ProfilesRoot => Path.Combine(AppRoot, "profiles");
    public string ProfilesFile => Path.Combine(AppRoot, "profiles.json");

    public ProfileStore()
    {
        Directory.CreateDirectory(AppRoot);
        Directory.CreateDirectory(ProfilesRoot);
    }

    public async Task<List<ProfileItem>> LoadAsync()
    {
        await _ioLock.WaitAsync();
        try
        {
            if (!File.Exists(ProfilesFile))
                return new List<ProfileItem>();

            await using var stream = File.OpenRead(ProfilesFile);
            var profiles = await JsonSerializer.DeserializeAsync<List<ProfileItem>>(stream, _jsonOptions)
                           ?? new List<ProfileItem>();

            // Migrate the old root URL to the current direct Dola chat route.
            foreach (var profile in profiles)
            {
                if (string.IsNullOrWhiteSpace(profile.HomeUrl) ||
                    profile.HomeUrl.Equals("https://www.dola.com/", StringComparison.OrdinalIgnoreCase) ||
                    profile.HomeUrl.Equals("https://dola.com/", StringComparison.OrdinalIgnoreCase))
                {
                    profile.HomeUrl = "https://www.dola.com/chat/";
                }
            }

            return profiles;
        }
        catch (Exception ex)
        {
            AppLogger.Error("Failed to load profiles.json", ex);
            throw;
        }
        finally
        {
            _ioLock.Release();
        }
    }

    public async Task SaveAsync(IEnumerable<ProfileItem> profiles)
    {
        await _ioLock.WaitAsync();
        try
        {
            Directory.CreateDirectory(AppRoot);
            var temp = ProfilesFile + ".tmp";
            var snapshot = profiles.ToList();

            await using (var stream = File.Create(temp))
            {
                await JsonSerializer.SerializeAsync(stream, snapshot, _jsonOptions);
                await stream.FlushAsync();
            }

            File.Move(temp, ProfilesFile, overwrite: true);
            AppLogger.Info($"Saved {snapshot.Count} profile(s).");
        }
        catch (Exception ex)
        {
            AppLogger.Error("Failed to save profiles.json", ex);
            throw;
        }
        finally
        {
            _ioLock.Release();
        }
    }

    public string GetProfileRoot(ProfileItem profile) => Path.Combine(ProfilesRoot, profile.Id);
    public string GetWebViewDataFolder(ProfileItem profile) => Path.Combine(GetProfileRoot(profile), "webview2");
    public string GetDownloadsFolder(ProfileItem profile) => Path.Combine(GetProfileRoot(profile), "downloads");

    public void EnsureProfileFolders(ProfileItem profile)
    {
        Directory.CreateDirectory(GetProfileRoot(profile));
        Directory.CreateDirectory(GetWebViewDataFolder(profile));
        Directory.CreateDirectory(GetDownloadsFolder(profile));
    }

    public void DeleteProfileData(ProfileItem profile)
    {
        var root = GetProfileRoot(profile);
        if (Directory.Exists(root))
            Directory.Delete(root, recursive: true);
    }
}
