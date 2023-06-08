using System;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using WebAPI.Data;
using WebAPI.Model;

namespace WebAPI.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class PersonController : ControllerBase
    {
        private readonly MyDbContext _context;

        public PersonController(MyDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult GetAll()
        {
            List<PersonModel> list = new List<PersonModel>();
            foreach (Person i in _context.Person.ToList())
            {
                PersonModel model = new PersonModel
                {
                    id_person = i.id_person,
                    active= i.active,
                    name = i.name,
                    gender = i.gender,
                    phoneNumber = i.phoneNumber,
                    email = i.email
                };
                list.Add(model);
            }
            return Ok(list);
        }


        [HttpGet]
        public IActionResult Filter(string text)
        {
            text = text.Trim();
            List<PersonModel> list = new List<PersonModel>();
            List<Person> list_Filter = new List<Person>();
            list_Filter = _context.Person.Where(
                x => Convert.ToString(x.id_person).Contains(text) == true ||
                x.name.Contains(text) == true ||
                x.email.Contains(text) == true ||
                x.phoneNumber.Contains(text) == true).ToList();
            if (list_Filter != null)
            {
                foreach (Person i in list_Filter)
                {
                    PersonModel model = new PersonModel
                    {
                        id_person = i.id_person,
                        active = i.active,
                        name = i.name,
                        gender = i.gender,
                        phoneNumber = i.phoneNumber,
                        email = i.email
                    };
                    list.Add(model);
                }
                return Ok(list);
            }
            else { return NotFound(); }
        }


        [HttpGet]
        public IActionResult GetById(int id)
        {
            Person person = _context.Person.FirstOrDefault(u => u.id_person == id);
            if (person == null)
            {
                return NotFound();
            }
            else
            {
                PersonModel model = new PersonModel
                {
                    id_person = person.id_person,
                    active = person.active,
                    name = person.name,
                    gender = person.gender,
                    phoneNumber = person.phoneNumber,
                    email = person.email
                };
                return Ok(model);
            }
        }

        [HttpPut]
        public IActionResult Put(PersonModel personModel)
        {
            Person person = _context.Person.FirstOrDefault(u => u.id_person == personModel.id_person);
            if (person == null)
            {
                return NotFound();
            }
            else
            {
                person.active = personModel.active;
                person.name = personModel.name;         
                person.gender = personModel.gender;
                person.phoneNumber = personModel.phoneNumber;
                person.email = personModel.email;
                _context.SaveChanges();
                return Ok();
            }
        }

        [HttpPut]
        public IActionResult PutActive(int id, bool active)
        {
            Person person = _context.Person.FirstOrDefault(u => u.id_person == id);
            if (person == null)
            {
                return NotFound();
            }
            else
            {
                person.active = active;
                _context.SaveChanges();
                return Ok();
            }
        }

        [HttpPost]
        public IActionResult Post(PersonModelPost model)
        {
            if (model == null)
            {
                return BadRequest();
            }
            else
            {
                Person person = new Person
                {
                    active = model.active,
                    name = model.name,
                    gender = model.gender,
                    phoneNumber = model.phoneNumber,
                    email = model.email,

                };
                _context.Person.Add(person);
                _context.SaveChanges();
                return Ok();
            }
        }

        [HttpDelete]
        public IActionResult Delete(int id)
        {
            Person person = _context.Person.FirstOrDefault(u => u.id_person == id);
            if (person == null)
            {
                return NotFound();
            }
            else
            {
                _context.Person.Remove(person);
                _context.SaveChanges();
                return Ok();
            }
        }
    }
}
