using Backend.models;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

namespace Backend.Helpers
{
    public interface ITokenService{
        string GenerateToken(User user);
    }
    public class TokenService : ITokenService
    {
        private readonly string _secretKey;
        private readonly string _issuer;
        private readonly int _expiryMinutes;

        public TokenService(string secretKey, string issuer, int expiryMinutes)
        {
            _secretKey = secretKey;
            _issuer = issuer;
            _expiryMinutes = expiryMinutes;
        }

        public string GenerateToken(User user)
        {
            // Create a claims identity with custom claims for the user's ID and username
            if (user.Username == null || user.Role == null)
            {
                throw new ArgumentNullException(nameof(user.Username));
            }
            var identity = new ClaimsIdentity(new[]
            {
                new Claim(ClaimTypes.NameIdentifier, user.UserID.ToString()),
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Role, user.Role)
                // Add any additional claims here, such as user roles
            });

            // Create the token descriptor with the signing key, issuer, audience, and expiration time
            var descriptor = new SecurityTokenDescriptor
            {
                Subject = identity,
                Expires = DateTime.UtcNow.AddMinutes(_expiryMinutes),
                SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secretKey)), SecurityAlgorithms.HmacSha256Signature),
                Issuer = _issuer,
                Audience = user.UserID.ToString() // Typically the audience is the intended recipient of the token, which is usually the same as the issuer in this case
            };

            // Create the token and serialize it to a string
            var handler = new JwtSecurityTokenHandler();
            var token = handler.CreateToken(descriptor);
            return handler.WriteToken(token);
        }
    }
}