using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Org.BouncyCastle.Bcpg;


namespace WebAPI.Model
{
    [Table("ParkingLot")]
    public class Parking
    {
        [Key]
        [Required]
        public string? number_plate { get; set; }

        [ForeignKey("number_plate")]
        public virtual Vehicle? Vehicle { get; set; }
    }
}
