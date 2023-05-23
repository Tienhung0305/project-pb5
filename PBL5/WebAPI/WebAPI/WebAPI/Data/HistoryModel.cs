using System.Drawing;
using System.Reflection.Metadata;


namespace WebAPI.Data
{
    public class HistoryModel
    {
        public string? id_history { get; set; }
        public bool isout { get; set; }
        public DateTime time { get; set; }
        public string? image { get; set; }
        public string? number_plate { get; set; }

    }
}
