import React, { useState, useEffect } from 'react';
import Popup from 'reactjs-popup';

const AdminBalance = (username) => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/myapp/api/get_admins_balance/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username: username.username }),
        });
        const data = await response.json();
        setTransactions(data.users);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };

    fetchTransactions();
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mt-8">Admin Transactions</h2>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b text-black">Username</th>
            <th className="py-2 px-4 border-b text-black">Money</th>
            <th className="py-2 px-4 border-b text-black">Out Trade No</th>
            <th className="py-2 px-4 border-b text-black">Real Money</th>
            <th className="py-2 px-4 border-b text-black">Percent</th>
            <th className="py-2 px-4 border-b text-black">Currency</th>
            <th className="py-2 px-4 border-b text-black">Pay Type</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td className="py-2 px-4 border-b text-black">{transaction.username}</td>
              <td className="py-2 px-4 border-b text-black">{transaction.money}</td>
              <td className="py-2 px-4 border-b text-black">{transaction.out_trade_no}</td>
              <td className="py-2 px-4 border-b text-black">{transaction.real_money}</td>
              <td className="py-2 px-4 border-b text-black">{transaction.percent}</td>
              <td className="py-2 px-4 border-b text-black">{transaction.currency}</td>
              <td className="py-2 px-4 border-b text-black">{transaction.pay_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminBalance;