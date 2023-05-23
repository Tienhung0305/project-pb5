using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Drawing;
using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;

namespace WebAPI.Model
{

    [Table("History")]
    public class History
    {
        [Key]
        [Required]
        public string? id_history { get; set; }
        public bool isout { get; set; }
        public DateTime time { get; set; }

        [MaxLength(800)]
        public string? image { get; set; }

        [MaxLength(100)]
        public string? number_plate { get;set; }

        [ForeignKey("number_plate")]
        public virtual Vehicle? Vehicle { get; set; }
    }
}
