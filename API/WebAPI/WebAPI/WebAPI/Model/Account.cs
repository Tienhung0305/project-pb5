using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace WebAPI.Model
{
    [Table("Account")]
    public class Account
    {
        [Key]
        [Required]
        public int id_account { get; set; }

        [MaxLength(100)]
        public string? username { get; set; }

        [MaxLength(100)]
        public string? password { get; set; }

    }
}
