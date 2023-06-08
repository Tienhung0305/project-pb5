using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace WebAPI.Model
{

    [Table("Vehicle")]
    public class Vehicle
    {
        [Key]
        [Required]
        [MaxLength(100)]
        public string? number_plate { get; set; }

        [MaxLength(100)]
        public string? car_manufacturer { get; set; }

        [MaxLength(100)]
        public string? name_vehide { get; set; }

        [MaxLength(100)]
        public string? color { get; set; }
        public int id_person { get; set; }

        [ForeignKey("id_person")]
        public virtual Person? Person { get; set; }

    }
}
