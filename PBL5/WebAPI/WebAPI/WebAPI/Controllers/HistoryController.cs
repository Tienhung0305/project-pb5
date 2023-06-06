using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using WebAPI.Data;
using WebAPI.Model;
using CloudinaryDotNet;
using CloudinaryDotNet.Actions;
using Microsoft.AspNetCore.Authentication;

namespace WebAPI.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class HistoryController : ControllerBase
    {
        private readonly MyDbContext _context;

        public HistoryController(MyDbContext context)
        {
            _context = context;
        }
        [HttpGet]
        public IActionResult GetAll()
        {
            List<HistoryModel> list = new List<HistoryModel>();
            foreach (History i in _context.History.ToList().OrderByDescending(p => p.time))
            {
                HistoryModel model = new HistoryModel
                {
                    id_history = i.id_history,
                    isout = i.isout,
                    time = i.time,
                    image = i.image,
                    number_plate = i.number_plate
                };
                list.Add(model);
            }
            return Ok(list);
        }

        [HttpGet]
        public IActionResult Filter(string text)
        {
            text = text.Trim();
            List<HistoryModel> list = new List<HistoryModel>();
            List<History> list_Filter = new List<History>();
            if(text == "Go_in")
            {
                list_Filter = _context.History.Where(x => x.isout == true).ToList();
            }
            else if (text == "Go_out")
            {
                list_Filter = _context.History.Where(x => x.isout == false).ToList();
            }
            else
            {
                list_Filter = _context.History.Where(x => x.id_history.Contains(text) == true || x.number_plate.Contains(text) == true).ToList();
            }
            if (list_Filter != null)
            {
                foreach (History i in list_Filter)
                {
                    HistoryModel model = new HistoryModel
                    {
                        id_history = i.id_history,
                        isout = i.isout,
                        time = i.time,
                        image = i.image,
                        number_plate = i.number_plate
                    };
                    list.Add(model);
                }
                return Ok(list);
            }
            else
            {
                return NotFound();
            }    
        }

        [HttpGet]
        public IActionResult GetById(string id)
        {
            History history = _context.History.FirstOrDefault(u => u.id_history == id);
            if (history == null)
            {
                return NotFound();
            }
            else
            {
                HistoryModel model = new HistoryModel
                {
                    id_history = history.id_history,
                    isout = history.isout,
                    time = history.time,
                    image = history.image,
                    number_plate = history.number_plate
                };
                return Ok(model);
            }
        }


        [HttpGet]
        public IActionResult CheckState(string number_plate)
        {
            History history = _context.History
           .Where(u => u.number_plate == number_plate)
           .OrderByDescending(p => p.time)
           .FirstOrDefault();
            if (history == null)
            {
                return NotFound();
            }
            else
            {
                HistoryModel model = new HistoryModel
                {
                    id_history = history.id_history,
                    isout = history.isout,
                    time = history.time,
                    image = history.image,
                    number_plate = history.number_plate
                };
                return Ok(model.isout);
            }
        }

   
        [HttpPut]
        public IActionResult Put(HistoryModelPut model)
        {
            History history = _context.History.FirstOrDefault(u => u.id_history == model.id_history);
            if (history == null)
            {
                return NotFound();
            }
            else
            {
                history.isout = model.isout;
                history.time = model.time;
                history.number_plate = model.number_plate;
                _context.SaveChanges();
                return Ok();
            }
        }

        [HttpPost]
        public IActionResult Post(HistoryModel model)
        {
            if (model == null)
            {
                return BadRequest();
            }
            else
            {
                History history = _context.History.FirstOrDefault(u => u.id_history == model.id_history);
                Vehicle vehicle = _context.Vehicles.FirstOrDefault(u => u.number_plate == model.number_plate);

                if (history != null && vehicle == null)
                {
                    return BadRequest();
                }
                else
                {
                    History history_t = new History
                    {
                        id_history = model.id_history,
                        isout = model.isout,
                        time = model.time,
                        image = model.image,
                        number_plate = model.number_plate
                    };
                    _context.History.Add(history_t);
                    _context.SaveChanges();
                    return Ok();
                }
            }
        }

        [HttpDelete]
        public IActionResult Delete(string id)
        {
            History history = _context.History.FirstOrDefault(u => u.id_history == id);
            if (history == null)
            {
                return NotFound();
            }
            else
            {
                var config = new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
                .Build();

                var cloudinaryConfig = config.GetSection("Cloudinary");
                var account = new CloudinaryDotNet.Account(
                    cloudinaryConfig["CloudName"],
                    cloudinaryConfig["ApiKey"],
                    cloudinaryConfig["ApiSecret"]
                );

                var cloudinary = new Cloudinary(account);

                var deletionParams = new DeletionParams(id);

                var result = cloudinary.Destroy(deletionParams);

                if (result.StatusCode == System.Net.HttpStatusCode.OK)
                {
                    _context.History.Remove(history);
                    _context.SaveChanges();
                    return Ok();
                }
                else
                {
                    return BadRequest();
                }
            }
        }


    }
}
