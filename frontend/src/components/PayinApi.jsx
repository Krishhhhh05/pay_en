import { useState } from 'react';
import axios from 'axios';
const PayinApi = () => {
  const [mchId, setMchId] = useState('1701');
  const [userName, setUserName] = useState('test');
  const [currency, setCurrency] = useState('BDT');
  const [payType, setPayType] = useState('BKASH');
  const [money, setMoney] = useState('1000');
  const [percent, setPercent] = useState('5');
  const [notifyUrl, setNotifyUrl] = useState('https://www.sandbox.wpay.one/callback/payin');
  const [returnUrl, setReturnUrl] = useState('https://www.google.com');
  const [data, setData] = useState('');
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // URL-encode the body
    const formBody = new URLSearchParams({
      mchId,
      userName,
      percent,
      currency,
      pay_type: payType,
      money,
      notify_url: notifyUrl,
      returnUrl,
    }).toString();
  
    console.log("Input body:", formBody);
  
    try {
      const response = await fetch('http://127.0.0.1:8000/myapp/api/payin_api/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formBody,
      });
  
      const data = await response.json();
      console.log(data);
      setData(data);
  
      // Show confirmation popup
      if (data.success) {
        const userConfirmed = window.confirm(`Do you want to be redirected to ${data.data.url}?`);
        if (userConfirmed) {
          window.location.href = data.returnUrl;
        }
  
        const callbackData =  JSON.stringify({

          mchId,
          userName,
          currency: "BDT",
          money,
          attach: "",
          pay_money: money,
          merchant_ratio: percent,
          real_money: (money - (money * (percent / 100))).toFixed(2),
          status: "1",
        });
  
        console.log('Callback data:', callbackData);
  
        setTimeout(async () => {
          try {
            // const callbackFormBody = new URLSearchParams(callbackData).toString();
            const callbackResponse = await fetch('http://127.0.0.1:8000/myapp/api/payin_callback/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: callbackData,
            });
  
            const responseData = await callbackResponse.json();
            console.log('Callback response:', callbackResponse);
            console.log('Callback response data:', responseData);
          } catch (callbackError) {
            console.error('Error calling payin_callback:', callbackError);
          }
        }, 5000);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  return (
    <div>
      <h2 className="text-xl font-bold">Payin API</h2>
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
          <label htmlFor="userName" className="block text-sm font-medium text-gray-700">UserName</label>
          <input
            type="text"
            id="userName"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
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
        {/* Additional fields for pay_type, money, notify_url, return_url */}
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
          <label htmlFor="percent" className="block text-sm font-medium text-gray-700">Percent</label>
          <input
            type="text"
            id="percent"
            value={percent}
            onChange={(e) => setPercent(e.target.value)}
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
          <label htmlFor="returnUrl" className="block text-sm font-medium text-gray-700">Return URL</label>
          <input
            type="text"
            id="returnUrl"
            value={returnUrl}
            onChange={(e) => setReturnUrl(e.target.value)}
            className="mt-1 p-2 border rounded-md w-full text-black"
            required
          />
        </div>
        <button type="submit" className="mt-4 p-2 bg-blue-500 text-white rounded-md">Submit</button>
      </form>
      {/* <div>{data.data}</div> */}
    </div>
  );
};

export default PayinApi;
