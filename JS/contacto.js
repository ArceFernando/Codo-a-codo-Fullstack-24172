

const userForm = document.querySelector('#userForm')

let users = []

window.addEventListener('DOMContentLoaded', async () => {
   const response = await fetch('/api/users');
   const data = await response.json()
   users = data
   renderUser(users)
      //method: 'GET'   
});

userForm.addEventListener('submit', async e => {
   e.preventDefault()

   const username = userForm['username'].value

   const response = await fetch('/api/users', {
      method: 'POST',
      headers: {
         'content-Type': 'application/json'
      },
      body: JSON.stringify({
         username: username 
      })
   }) 

   const data = await response.json();

   users.push(data)

   renderUser(users)

   userForm.reset();
})

function renderUser(users) {
   const userList = document.querySelector('#userList')
   userList.innerHTML = ''

   users.forEach(user => {
      const userItem = document.createElement('li')
      userItem.innerHTML = `
         <h6>${user.username}</h6>
      `
      userList.append(UserItem)
   })
}

