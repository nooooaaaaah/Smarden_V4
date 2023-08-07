namespace Backend.models
{
    public class Plant
    {
        public int PlantID { get; set; }
        public string? CommonName { get; set; }
        public DateTime Created { get; set; }
        public DateOnly DatePlanted { get; set; }
        public int UserID { get; set; }
        public User? User { get; private set; }

        public void SetUser(User user)
        {
            User = user ?? throw new ArgumentNullException(nameof(user));
            UserID = user.UserID;
        }

        public void SetCommonName(string commonname)
        {
            CommonName = commonname ?? throw new ArgumentNullException(nameof(commonname));
        }
    }
}