using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using WebAPI.Data;
using WebAPI.Model;

namespace WebAPI.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class VehicleController : ControllerBase
    {
        private readonly MyDbContext? _context;

        public VehicleController(MyDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult CheckInvalid(string number_plate)
        {
            foreach(var item in _context.Vehicles.ToList())
            {
                if(item.number_plate == number_plate)
                {
                    return Ok(item);
                }
            }
            return BadRequest(number_plate);
        }

        [HttpGet]
        public IActionResult Filter(string text)
        {
            text = text.Trim();
            List<VehicleModel> list = new List<VehicleModel>();
            List<Vehicle> list_Filter = new List<Vehicle>();
            list_Filter = _context.Vehicles.Where(
                x => x.number_plate.Contains(text) == true ||
                x.car_manufacturer.Contains(text) == true ||
                x.name_vehide.Contains(text) == true ||
                x.color.Contains(text) == true).ToList();
            if (list_Filter != null)
            {
                foreach (Vehicle i in list_Filter)
                {
                    VehicleModel model = new VehicleModel
                    {
                        number_plate = i.number_plate,
                        car_manufacturer = i.car_manufacturer,
                        name_vehide = i.name_vehide,
                        color = i.color,
                        id_person = i.id_person,
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
        public IActionResult GetAll()
        {
            List<VehicleModel> list = new List<VehicleModel>();
            foreach (Vehicle i in _context.Vehicles.ToList())
            {
                VehicleModel model = new VehicleModel
                {
                    number_plate = i.number_plate,
                    car_manufacturer = i.car_manufacturer,              
                    name_vehide = i.name_vehide,
                    color = i.color,
                    id_person = i.id_person,
                };
                list.Add(model);
            }
            return Ok(list);
        }

        [HttpGet]
        public IActionResult GetByNumberPlate(string number_plate)
        {
            Vehicle vehicle = _context.Vehicles.FirstOrDefault(u => u.number_plate == number_plate);
            if (vehicle == null)
            {
                return NotFound();
            }
            else
            {
                VehicleModel model = new VehicleModel
                {
                    number_plate = number_plate,
                    car_manufacturer = vehicle.car_manufacturer,
                    name_vehide = vehicle.name_vehide,
                    color = vehicle.color,        
                    id_person = vehicle.id_person             
                };
                return Ok(model);
            }
        }

        [HttpGet]

        public IActionResult CheckByIdProfile(int id_profile)
        {
            bool check = false;
            foreach (Vehicle vehicle in _context.Vehicles.ToList())
            {
                if (vehicle.id_person == id_profile)
                {
                    check = true; break;
                }    
            }    
            return Ok(check);
        }

        [HttpPut]
        public IActionResult Put(VehicleModel vehicleModel)
        {
            Vehicle vehicle = _context.Vehicles.FirstOrDefault(u => u.number_plate == vehicleModel.number_plate);
            Person person = _context.Person.FirstOrDefault(u => u.id_person == vehicleModel.id_person);
            if (vehicle == null || person == null)
            {
                return NotFound();
            }
            else
            {
                vehicle.car_manufacturer = vehicleModel.car_manufacturer;
                vehicle.name_vehide = vehicleModel.name_vehide;
                vehicle.color = vehicleModel.color;
                vehicle.id_person = vehicleModel.id_person;
                _context.SaveChanges();
                return Ok();
            }
        }

        [HttpPost]
        public IActionResult Post(VehicleModel model)
        {
            Person person = _context.Person.FirstOrDefault(u => u.id_person == model.id_person);
            if (model == null || person == null)
            {
                return BadRequest();
            }
            else
            {
                Vehicle vehicle = new Vehicle
                {
                    number_plate = model.number_plate,
                    car_manufacturer = model.car_manufacturer,
                    name_vehide = model.name_vehide, 
                    color = model.color, 
                    id_person = model.id_person
                };
                _context.Vehicles.Add(vehicle);
                _context.SaveChanges();
                return Ok();
            }
        }

        [HttpDelete]
        public IActionResult Delete(string number_plate)
        {
            Vehicle vehicle = _context.Vehicles.FirstOrDefault(u => u.number_plate == number_plate);
            if (vehicle == null)
            {
                return NotFound();
            }
            else
            {
                _context.Vehicles.Remove(vehicle);
                _context.SaveChanges();
                return Ok();
            }
        }

    }
}
