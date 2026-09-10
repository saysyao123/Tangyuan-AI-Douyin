using Microsoft.Web.WebView2.Core;
using TangyuanDolaStudio.Models;

namespace TangyuanDolaStudio.Services;

public sealed class BrowserInstanceManager
{
    private readonly ProfileStore _profileStore;
    private readonly Dictionary<string, CoreWebView2Environment> _environments = new();

    public BrowserInstanceManager(ProfileStore profileStore)
    {
        _profileStore = profileStore;
    }

    public async Task<CoreWebView2Environment> GetEnvironmentAsync(ProfileItem profile)
    {
        if (_environments.TryGetValue(profile.Id, out var existing))
            return existing;

        _profileStore.EnsureProfileFolders(profile);
        var userDataFolder = _profileStore.GetWebViewDataFolder(profile);
        var environment = await CoreWebView2Environment.CreateAsync(
            browserExecutableFolder: null,
            userDataFolder: userDataFolder,
            options: new CoreWebView2EnvironmentOptions());

        _environments[profile.Id] = environment;
        return environment;
    }

    public string GetDownloadsFolder(ProfileItem profile)
    {
        _profileStore.EnsureProfileFolders(profile);
        return _profileStore.GetDownloadsFolder(profile);
    }

    public void Forget(ProfileItem profile)
    {
        _environments.Remove(profile.Id);
    }
}
