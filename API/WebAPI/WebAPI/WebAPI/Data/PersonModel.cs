namespace WebAPI.Data
{
    public class PersonModel
    {
        public int id_person { get; set; }
        public bool? active { get; set; }
        public string? name { get; set; }
        public string? gender { get; set; }
        public string? phoneNumber { get; set; }
        public string? email { get; set; }
    }
}
