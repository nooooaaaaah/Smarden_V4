# Example implantation of the Authorization and Authentication module in .net7

## To implement authorization in .NET Core 7 for your backend API, you can follow these steps

### Define the authorization policy: In your application, define one or more policies that describe the authorization requirements for different resources. For example, you might have a policy that allows access only to authenticated users, and another policy that allows access only to users with certain roles.

```c#
services.AddAuthorization(options =>
{
    options.AddPolicy("RequireAuthenticatedUser", policy =>
    {
        policy.RequireAuthenticatedUser();
    });

    options.AddPolicy("RequireAdminRole", policy =>
    {
        policy.RequireRole("admin");
    });
});
```

### Add the authentication middleware: You need to add the authentication middleware to your pipeline before the authorization middleware. Here is an example

```c
app.UseAuthentication();
app.UseAuthorization();
```

#### Alternatively, you can apply the authorization policy in your middleware pipeline

```c#
app.Use(async (context, next) =>
{
    var authService = context.RequestServices.GetRequiredService<IAuthorizationService>();

    var result = await authService.AuthorizeAsync(context.User, null, "RequireAdminRole");
    if (!result.Succeeded)
    {
        context.Response.StatusCode = 403; // Forbidden
        return;
    }

    await next();
});
```
