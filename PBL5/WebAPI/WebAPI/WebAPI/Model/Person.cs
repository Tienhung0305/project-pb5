using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;


namespace WebAPI.Model
{
    [Table("Person")]
    public class Person
    {
        [Key]
        [Required]
        public int id_person { get; set; }
        public bool? active { get; set; }

        [MaxLength(100)]
        public string? name { get; set; }
        public string? gender { get; set; }

        [MaxLength(100)]
        public string? phoneNumber { get; set; }

        [MaxLength(100)]
        public string? email { get; set; }

        public ICollection<Vehicle>? Vehicle { get; set; }

    }
}
