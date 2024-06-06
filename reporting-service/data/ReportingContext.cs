using Microsoft.EntityFrameworkCore;
using ReportingService.Models;

namespace ReportingService.Data
{
    public class ReportingContext : DbContext
    {
        public ReportingContext(DbContextOptions<ReportingContext> options) : base(options) { }

        public DbSet<Report> Reports { get; set; }
    }
}
