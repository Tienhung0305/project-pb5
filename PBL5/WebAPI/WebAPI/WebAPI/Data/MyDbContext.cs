using Microsoft.EntityFrameworkCore;
using WebAPI.Model;

namespace WebAPI.Data
{
    public class MyDbContext : DbContext
    {
        public MyDbContext(DbContextOptions<MyDbContext> options) :
            base(options)
        { }
        
        public DbSet<Account>? Account { get; set; }
        public DbSet<Person>? Person { get; set; }
        public DbSet<Vehicle>? Vehicles { get; set; }
        public DbSet<History>? History { get; set; }

    }
}
