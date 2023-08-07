using Backend.Helpers;
using Backend.models;
using Microsoft.EntityFrameworkCore;

namespace Backend.Services
{
    public interface IUserService
    {
        Task<User> Authenticate(string username, string password);
        Task<IEnumerable<User>> GetAll();
        Task<User> GetById(int id);
        Task<User> Create(User user, string password);
        Task Update(User user, string? password = null);
        Task Delete(int id);
    }

    public class UserService : IUserService
    {
        private readonly SmardenDbContext _context;

        public UserService(SmardenDbContext context)
        {
            _context = context;
        }

        public async Task<User> Authenticate(string username, string password)
        {
            if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
                throw new AppException("Username or Password Empty");
            if (_context.Users == null)
            {
                throw new AppException("Error: Null User");
            }
            var user = await _context.Users.SingleOrDefaultAsync(x => x.Username == username);

            if (user == null || user.PasswordHash == null || user.PasswordSalt ==null)
                throw new AppException("Error: Null User");

            if (!PasswordHasher.VerifyPasswordHash(password, user.PasswordHash, user.PasswordSalt))
                throw new AppException("Error: Null User");

            return user;
        }

        public async Task<IEnumerable<User>> GetAll()
        {
            if (_context.Users == null)
            {
                throw new AppException("Error: Null User");
            }
            return await _context.Users.ToListAsync();
        }

        public async Task<User> GetById(int id)
        {
            if (_context.Users == null)
            {
                throw new AppException("Error: Null User");
            }
            return await _context.Users.FindAsync(id) ?? throw new AppException("Error returning User");
        }

        public async Task<User> Create(User user, string password)
        {
            if (string.IsNullOrWhiteSpace(password))
                throw new AppException("Password is required");
            if(_context.Users == null){
                throw new AppException("Error: Null User");
            }

            if (await _context.Users.AnyAsync(x => x.Username == user.Username))
                throw new AppException("Username \"" + user.Username + "\" is already taken");

            byte[] passwordHash, passwordSalt;
            PasswordHasher.CreatePasswordHash(password, out passwordHash, out passwordSalt);

            user.PasswordHash = passwordHash;
            user.PasswordSalt = passwordSalt;

            await _context.Users.AddAsync(user);
            await _context.SaveChangesAsync();

            return user;
        }

        public async Task Update(User userParam, string? password = null)
        {
            if (_context.Users == null)
            {
                throw new AppException("Error: Null User");
            }
            var user = await _context.Users.FindAsync(userParam.UserID);

            if (user == null)
                throw new AppException("User not found");

            if (userParam.Username != user.Username)
            {
                if (await _context.Users.AnyAsync(x => x.Username == userParam.Username))
                    throw new AppException("Username " + userParam.Username + " is already taken");
            }

            user.FirstName = userParam.FirstName;
            user.LastName = userParam.LastName;
            user.Username = userParam.Username;
            user.Role = userParam.Role;

            if (!string.IsNullOrWhiteSpace(password))
            {
                PasswordHasher.CreatePasswordHash(password, out byte[] passwordHash, out byte[] passwordSalt);

                user.PasswordHash = passwordHash;
                user.PasswordSalt = passwordSalt;
            }

            _context.Users.Update(user);
            await _context.SaveChangesAsync();
        }

        public async Task Delete(int id)
        {
            if (_context.Users == null)
            {
                throw new AppException("Error: Null User");
            }
            var user = await _context.Users.FindAsync(id);
            if (user != null)
            {
                _context.Users.Remove(user);
                await _context.SaveChangesAsync();
            }
        }
    }
}

