using System.Security.Cryptography;
using System.Text;

namespace Backend.Helpers
{
    public class PasswordHasher
    {
        public static byte[] GenerateRandomSalt(int saltLength)
        {
            byte[] salt = new byte[saltLength];
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(salt);
            }
            return salt;
        }

        public static void CreatePasswordHash(string password, out byte[] passwordHash, out byte[] passwordSalt)
        {
            if (password == null) throw new ArgumentNullException(nameof(password));
            if (string.IsNullOrWhiteSpace(password)) throw new ArgumentException("Value cannot be empty or whitespace only string.", nameof(password));
            passwordSalt = GenerateRandomSalt(24);
            using var sha256 = SHA256.Create();
            passwordHash = sha256.ComputeHash(Encoding.UTF8.GetBytes(password).Concat(passwordSalt).ToArray());
        }


        public static bool VerifyPasswordHash(string password, byte[] storedHash, byte[] storedSalt)
        {
            if (password == null) throw new ArgumentNullException(nameof(password));
            if (storedHash == null) throw new ArgumentNullException(nameof(storedHash));
            if (storedSalt == null) throw new ArgumentNullException(nameof(storedSalt));

            if (storedHash.Length != 32) throw new ArgumentException("Invalid length of password hash (32 bytes expected).", nameof(storedHash));
            if (storedSalt.Length != 24) throw new ArgumentException("Invalid length of password salt (16 bytes expected).", nameof(storedSalt));

            using var sha256 = SHA256.Create();
            var hash = sha256.ComputeHash(Encoding.UTF8.GetBytes(password).Concat(storedSalt).ToArray());
            // Compare the computed hash with the stored hash
            for (int i = 0; i < hash.Length; i++)
            {
                if (hash[i] != storedHash[i]) return false;
            }

            // If the hashes match, the password is valid
            return true;
        }
    }
}