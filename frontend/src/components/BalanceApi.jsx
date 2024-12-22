// components/BalanceApi.js
import { useState } from 'react';
import 'reactjs-popup/dist/index.css';
import Popup from 'reactjs-popup';

const BalanceApi = () => {
  const [mchId, setMchId] = useState('');
  const [currency, setCurrency] = useState('');
  const [apiData,setApiData]=useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const body = JSON.stringify({ mchId, currency });
 


    try {
      const response = await fetch('http://127.0.0.1:8000/myapp/api/get_balance/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body
      });

      const data = await response.json();
      console.log(data);
      console.log("data",data.balance[0].balance);
      setApiData(data.balance[0].balance);

    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
    <h2 className="text-xl font-bold">Get Balance</h2>
    <form onSubmit={handleSubmit} className="space-y-4 p-4">
      <div>
        <label htmlFor="mchId" className="block text-sm font-medium text-gray-700">Merchant ID</label>
        <input
          type="text"
          id="mchId"
          value={mchId}
          onChange={(e) => setMchId(e.target.value)}
          className="mt-1 p-2 border rounded-md w-full text-black"
          required
        />
      </div>
      <div>
        <label htmlFor="currency" className="block text-sm font-medium text-gray-700">Currency</label>
        <input
          type="text"
          id="currency"
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          className="mt-1 p-2 border rounded-md w-full"
          required
        />
      </div>
         <button type="submit" className="mt-4 p-2 bg-blue-500 text-white rounded-md">Submit</button>
         <div>{apiData}</div>
 

    </form>
    
    </div>
  );
};

export default BalanceApi;
