using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebAPI.Data;
using WebAPI.Model;

namespace WebAPI.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class AccountsController : ControllerBase
    {
        private readonly MyDbContext _context;

        public AccountsController(MyDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult GetAll()
        {
            return Ok(_context.Account.ToList());
        }

        [HttpGet]
        public IActionResult Login(string username, string password)
        {
            Account account = _context.Account.FirstOrDefault(u => u.username == username && u.password == password);
            if (account == null)
            {
                return NotFound();
            }
            else
            {
                AccountModel model = new AccountModel
                {
                    username = username,
                    password = password
                };
                return Ok(model);
            }
        }

        [HttpPost]
        public IActionResult Post(AccountModel model)
        {
            if (model == null)
            {
                return BadRequest();
            }
            else
            {
                Account account = _context.Account.FirstOrDefault(u => u.username == model.username);
                if (account == null)
                {
                    Account acc = new Account
                    {
                        username = model.username,
                        password = model.password
                    };
                    _context.Account.Add(acc);
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
