import React, { useState, useEffect } from 'react';

const CreateAdmin = () => {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [percent, setPercent] = useState('');
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    const firstFetchUsers = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/myapp/api/get_users');
        const data = await response.json();
        setUsers(data.users);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
    firstFetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/myapp/api/get_users');
      const data = await response.json();
      setUsers(data.users);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("New Admin");
    try {
      const response = await fetch('http://127.0.0.1:8000/myapp/api/create_admin/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          percent,
        }),
      });

      const data = await response.json();
      console.log(data);
      setShowForm(false);
      setUsername('');
      setPassword('');
      setPercent('');
      fetchUsers();
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const removeUser = async (username) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/myapp/api/remove_admin/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
        }),
      });
      fetchUsers();
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2 className="text-xl font-bold">Users</h2>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="py-2 text-black">ID</th>
            <th className="py-2 text-black">Username</th>
            <th className="py-2 text-black">Percent</th>
            <th className="py-2 text-black">Role</th>
            <th className="py-2 text-black">Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={user.username}>
              <td className="border px-4 py-2 text-black">{index + 1}</td>
              <td className="border px-4 py-2 text-black">{user.username}</td>
              <td className="border px-4 py-2 text-black">{user.percent}</td>
              <td className="border px-4 py-2 text-black">{user.role}</td>
              <td className="border px-4 py-2 text-black">
                <button
                  onClick={() => removeUser(user.username)}
                  className="p-2 bg-red-500 text-white rounded-md"
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => setShowForm(true)} className="mt-4 p-2 bg-blue-500 text-white rounded-md">
        Create New Admin
      </button>
      {showForm && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-md shadow-md">
            <h2 className="text-xl font-bold mb-4 text-black">Create Admin</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="mt-1 p-2 border rounded-md w-full text-black"
                  required
                />
              </div>
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="mt-1 p-2 border rounded-md w-full text-black"
                  required
                />
              </div>
              <div>
                <label htmlFor="percent" className="block text-sm font-medium text-gray-700">Percent</label>
                <input
                  type="number"
                  id="percent"
                  value={percent}
                  onChange={(e) => setPercent(e.target.value)}
                  className="mt-1 p-2 border rounded-md w-full text-black"
                  required
                />
              </div>
              <div className="flex justify-end space-x-4">
                <button type="button" onClick={() => setShowForm(false)} className="p-2 bg-gray-500 text-white rounded-md">
                  Cancel
                </button>
                <button type="submit" className="p-2 bg-blue-500 text-white rounded-md">
                  Create Admin
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CreateAdmin;