using CloudinaryDotNet.Actions;
using CloudinaryDotNet;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using WebAPI.Data;
using WebAPI.Model;

namespace WebAPI.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class ParkingController : ControllerBase
    {

        private readonly MyDbContext _context;

        public ParkingController(MyDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult GetAll()
        {
            List<ParkingModel> list = new List<ParkingModel>();
            foreach (Parking i in _context.Parking.ToList())
            {
                ParkingModel model = new ParkingModel
                {
                    number_plate = i.number_plate
                };
                list.Add(model);
            }
            return Ok(list);
        }

        [HttpGet]
        public IActionResult GetNumberParked()
        {
            return Ok(_context.Parking.ToList().Count());
        }

        [HttpPost]
        public IActionResult Post(ParkingModel model)
        {
            if (model == null)
            {
                return BadRequest();
            }
            else
            {
                Vehicle vehicle = _context.Vehicles.FirstOrDefault(u => u.number_plate == model.number_plate);
                if (vehicle == null)
                {
                    return BadRequest();
                }
                else
                {
                    Parking parking = new Parking
                    {
                        number_plate = model.number_plate,
                    };
                    _context.Parking.Add(parking);
                    _context.SaveChanges();
                    return Ok();
                }
            }
        }

        [HttpDelete]
        public IActionResult Delete(string number_plate)
        {
            Parking parking = _context.Parking.FirstOrDefault(u => u.number_plate == number_plate);
            if (parking == null)
            {
                return NotFound();
            }
            else
            {                      
            _context.Parking.Remove(parking);
            _context.SaveChanges();
            return Ok();  
            }
        }

        [HttpGet]
        public IActionResult CheckState(string number_plate)
        {
            Parking parking = _context.Parking
           .Where(u => u.number_plate == number_plate)
           .FirstOrDefault();
            if (parking == null)
            {
                return Ok(true);
            }
            else
            {
                return Ok(false);
            }
        }



    }
}
