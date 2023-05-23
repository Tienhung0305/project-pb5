namespace WebAPI.Data
{
    public class HistoryModelPut
    {
        public string? id_history { get; set; }
        public bool isout { get; set; }
        public DateTime time { get; set; }
        public string? number_plate { get; set; }

    }
}
