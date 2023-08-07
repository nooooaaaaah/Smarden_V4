using Microsoft.EntityFrameworkCore;
using Backend.models;

namespace Backend.Helpers;

public partial class SmardenDbContext : DbContext
{
    public SmardenDbContext()
    {
    }

    public SmardenDbContext(DbContextOptions<SmardenDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Plant>? Plants { get; set; }
    public virtual DbSet<User>? Users { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Plant>(entity =>
        {
            entity.HasKey(e => e.PlantID);
            entity.Property(e => e.CommonName).IsRequired();
            entity.Property(e => e.Created).IsRequired();
            entity.Property(e => e.DatePlanted).IsRequired();
            entity.HasOne(e => e.User).WithMany(u => u.UserPlants).HasForeignKey(e => e.UserID).IsRequired();
        });
        modelBuilder.Entity<Plant>(entity =>
        {
            entity.Property(e => e.CommonName)
                .IsRequired()
                .HasMaxLength(50);

            entity.Property(e => e.Created)
                .HasColumnType("timestamp without time zone")
                .HasDefaultValueSql("now()");

            entity.Property(e => e.DatePlanted)
                .HasColumnType("date");

            entity.HasOne(d => d.User)
                .WithMany(p => p.UserPlants)
                .HasForeignKey(d => d.UserID)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("fk_plant_user");
        });
        OnModelCreatingPartial(modelBuilder);
    }
    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
