using System.IO;
using System.Text.Json;
using TangyuanDolaStudio.Models;

namespace TangyuanDolaStudio.Services;

public sealed class ProfileStore
{
    private readonly JsonSerializerOptions _jsonOptions = new()
    {
        WriteIndented = true
    };

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
        if (!File.Exists(ProfilesFile))
            return new List<ProfileItem>();

        await using var stream = File.OpenRead(ProfilesFile);
        return await JsonSerializer.DeserializeAsync<List<ProfileItem>>(stream, _jsonOptions)
               ?? new List<ProfileItem>();
    }

    public async Task SaveAsync(IEnumerable<ProfileItem> profiles)
    {
        Directory.CreateDirectory(AppRoot);
        await using var stream = File.Create(ProfilesFile);
        await JsonSerializer.SerializeAsync(stream, profiles, _jsonOptions);
    }

    public string GetProfileRoot(ProfileItem profile)
        => Path.Combine(ProfilesRoot, profile.Id);

    public string GetWebViewDataFolder(ProfileItem profile)
        => Path.Combine(GetProfileRoot(profile), "webview2");

    public string GetDownloadsFolder(ProfileItem profile)
        => Path.Combine(GetProfileRoot(profile), "downloads");

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
