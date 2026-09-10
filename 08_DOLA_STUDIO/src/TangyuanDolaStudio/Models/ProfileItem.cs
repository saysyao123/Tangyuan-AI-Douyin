namespace TangyuanDolaStudio.Models;

public sealed class ProfileItem
{
    public string Id { get; set; } = Guid.NewGuid().ToString("N");
    public string DisplayName { get; set; } = "Dola";
    public string HomeUrl { get; set; } = "https://www.dola.com/";
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.Now;
    public DateTimeOffset? LastOpenedAt { get; set; }

    public override string ToString() => DisplayName;
}
