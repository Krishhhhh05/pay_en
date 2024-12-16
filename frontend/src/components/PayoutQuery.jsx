// components/PayoutQuery.js
import { useState } from 'react';
const PayoutQuery = () => {
    const [mchId, setMchId] = useState('1000');
    const [outTradeNo, setOutTradeNo] = useState('20241217024756');
  const [response, setResponse] = useState('');
    const handleSubmit = async (e) => {
      e.preventDefault();
      const body = JSON.stringify({ mchId, out_trade_no: outTradeNo });
      console.log('Payout Query:', body);
  
      try {
        const response = await fetch('http://127.0.0.1:8000/myapp/api/payout_query/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body
        });
  
        const data = await response.json();
        console.log(data);
        setResponse(JSON.stringify(data, null, 2));
      } catch (error) {
        console.error('Error:', error);
      }
    };
  
    return (
      <div>
      <h2 className="text-xl font-bold">Payout Query</h2>
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
          <label htmlFor="outTradeNo" className="block text-sm font-medium text-gray-700">Order ID</label>
          <input
            type="text"
            id="outTradeNo"
            value={outTradeNo}
            onChange={(e) => setOutTradeNo(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <button type="submit" className="mt-4 p-2 bg-blue-500 text-white rounded-md">Submit</button>
      </form>
{response}
      </div>
    );
  };
  
  export default PayoutQuery;
  