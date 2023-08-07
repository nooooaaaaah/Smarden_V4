namespace Backend.models
{
    public class User
    {
        public int UserID { get; set; }
        public string? Username { get; set; }
        public string? FirstName { get; set; }
        public string? LastName { get; set; }
        public string? Role { get; set; } // Renamed property
        public byte[]? PasswordHash { get; set; }
        public byte[]? PasswordSalt { get; set; }

        private List<Plant>? Plants { get; set; }
        public IReadOnlyCollection<Plant>? UserPlants => Plants?.AsReadOnly();

        private static readonly string SpecialChars = @"%!#$%^&*()?/><,|}]{~`+=";

        /// Sets user information and validates input.
        public void SetUser(string username, string firstname, string lastname, string password)
        {
            Username = username;
            FirstName = firstname;
            LastName = lastname;
            if (string.IsNullOrEmpty(username) || username.Any(c => SpecialChars.Contains(c)))
            {
                throw new ArgumentException("A valid Username must be provided");
            }
            if (string.IsNullOrEmpty(firstname) || firstname.Any(c => SpecialChars.Contains(c))) // Fixed validation
            {
                throw new ArgumentException("A valid First Name must be provided");
            }
            if (string.IsNullOrEmpty(lastname) || lastname.Any(c => SpecialChars.Contains(c))) // Fixed validation
            {
                throw new ArgumentException("A valid Last Name must be provided");
            }
            if (string.IsNullOrEmpty(Role))
            {
                throw new ArgumentException("Role must be provided");
            }
        }

        /// Sets the list of plants associated with the user.
        public void SetPlant(List<Plant> plants)
        {
            Plants = plants ?? throw new ArgumentNullException(nameof(plants));
        }
    }
}