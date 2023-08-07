using System.Text;
using Backend.Helpers;
using Backend.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Add the configuration data to the service container
var configuration = builder.Configuration;
builder.Services.AddSingleton(configuration);

//Authorization
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("test", policy =>
    {
        policy.AuthenticationSchemes.Add(JwtBearerDefaults.AuthenticationScheme);
        policy.RequireAuthenticatedUser();
        policy.RequireClaim(ClaimTypes.Role, "test");
    });
});

builder.Services.AddDbContext<SmardenDbContext>(opt =>
    opt.UseNpgsql(configuration.GetConnectionString("WebApiDatabase")));

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// JWT
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.RequireHttpsMetadata = false;
        options.SaveToken = true;
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.ASCII.GetBytes("your-secret-key-12345678")),
            ValidateIssuer = false,
            ValidateAudience = false
        };
    });

// my services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<ITokenService>(sp =>
    new TokenService(
        secretKey: "your-secret-key-12345678",
        issuer: "your-issuer",
        expiryMinutes: 60 // or any other value you prefer
    ));

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
        {
            options.SwaggerEndpoint("/swagger/v1/swagger.json", "v1");
            options.RoutePrefix = string.Empty;
        }
    );
}

app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
