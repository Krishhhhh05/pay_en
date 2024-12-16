// components/PayoutApi.js
import { useState } from 'react';
const PayoutApi = () => {
    const [mchId, setMchId] = useState('1000');
    const [currency, setCurrency] = useState('PKR');
    const [payType, setPayType] = useState('JAZZCASH');
    const [account, setAccount] = useState('03123456789');
    const [username, setUsername] = useState('ramesh.sutar');
    const [money, setMoney] = useState('500');
    const [notifyUrl, setNotifyUrl] = useState('callback_payout_url');
    const [reserve1, setReserve1] = useState('1234567890123');
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      const body = JSON.stringify({
        mchId, currency, pay_type: payType, account, userName: username, money, notify_url: notifyUrl, reserve1
      });
  
      try {
        const response = await fetch('http://127.0.0.1:8000/myapp/api/payout_api/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body
        });
  
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };
  
    return (
        <div>
        <h2 className="text-xl font-bold">Payout API</h2>
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
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <div>
          <label htmlFor="payType" className="block text-sm font-medium text-gray-700">Payment Type</label>
          <input
            type="text"
            id="payType"
            value={payType}
            onChange={(e) => setPayType(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <div>
          <label htmlFor="account" className="block text-sm font-medium text-gray-700">Account</label>
          <input
            type="text"
            id="account"
            value={account}
            onChange={(e) => setAccount(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
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
          <label htmlFor="money" className="block text-sm font-medium text-gray-700">Amount</label>
          <input
            type="text"
            id="money"
            value={money}
            onChange={(e) => setMoney(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <div>
          <label htmlFor="notifyUrl" className="block text-sm font-medium text-gray-700">Notify URL</label>
          <input
            type="text"
            id="notifyUrl"
            value={notifyUrl}
            onChange={(e) => setNotifyUrl(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <div>
          <label htmlFor="reserve1" className="block text-sm font-medium text-gray-700">Reserve 1</label>
          <input
            type="text"
            id="reserve1"
            value={reserve1}
            onChange={(e) => setReserve1(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <button type="submit" className="mt-4 p-2 bg-blue-500 text-white rounded-md">Submit</button>
      </form>
      </div>
    );
  };
  
  export default PayoutApi;
  