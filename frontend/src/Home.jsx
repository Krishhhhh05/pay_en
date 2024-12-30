import React, { useState } from 'react';
import BalanceApi from './components/BalanceApi';
import PayinQuery from './components/PayinQuery';
import PayinApi from './components/PayinApi';
import PayoutApi from './components/PayoutApi';
import PayoutQuery from './components/PayoutQuery';
import CreateAdmin from './components/CreateAdmin';

const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-gray-800 text-white rounded-lg p-6 shadow-lg">
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-white"
          onClick={onClose}
        >
          &times;
        </button>
        {children}
      </div>
    </div>
  );
};

const Home = () => {
  const [activeTab, setActiveTab] = useState('balance'); // Manage active tab state
  const [payinData, setPayinData] = useState(null); // Manage payin data
  const [modalContent, setModalContent] = useState(null); // Modal content state
  const [isModalOpen, setIsModalOpen] = useState(false); // Modal visibility state

  // Handler for successful Payin API submission
  const handlePayinSuccess = (data) => {
    setPayinData(data); // Set the Payin data for use in PayinQuery and PayoutApi
    setActiveTab('payinQuery'); // Automatically switch to PayinQuery tab on success
  };

  // Handler for opening the modal with content
  const handleOpenModal = (content) => {
    setModalContent(content);
    setIsModalOpen(true);
  };

  // Handler for closing the modal
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setModalContent(null);
  };

  return (
    <div className="p-8 bg-gray-900 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Forms</h1>

      {/* Tab navigation */}
      <div className="flex space-x-4 border-b border-gray-700 mb-6">
        <button
          className={`px-4 py-2 rounded-t-md text-sm font-medium transition-colors duration-300 ${
            activeTab === 'balance'
              ? 'bg-gray-800 text-white border-b-2 border-blue-500'
              : 'bg-gray-700 text-gray-300 hover:text-white'
          }`}
          onClick={() => setActiveTab('balance')}
        >
          Balance
        </button>
        <button
          className={`px-4 py-2 rounded-t-md text-sm font-medium transition-colors duration-300 ${
            activeTab === 'payin'
              ? 'bg-gray-800 text-white border-b-2 border-blue-500'
              : 'bg-gray-700 text-gray-300 hover:text-white'
          }`}
          onClick={() => setActiveTab('payin')}
        >
          Payin
        </button>
        <button
          className={`px-4 py-2 rounded-t-md text-sm font-medium transition-colors duration-300 ${
            activeTab === 'payout'
              ? 'bg-gray-800 text-white border-b-2 border-blue-500'
              : 'bg-gray-700 text-gray-300 hover:text-white'
          }`}
          onClick={() => setActiveTab('payout')}
        >
          Payout
        </button>
        <button
          className={`px-4 py-2 rounded-t-md text-sm font-medium transition-colors duration-300 ${
            activeTab === 'payinQuery'
              ? 'bg-gray-800 text-white border-b-2 border-blue-500'
              : 'bg-gray-700 text-gray-300 hover:text-white'
          }`}
          onClick={() => setActiveTab('payinQuery')}
        >
          Payin Query
        </button>

        <button
          className={`px-4 py-2 rounded-t-md text-sm font-medium transition-colors duration-300 ${
            activeTab === 'payoutQuery'
              ? 'bg-gray-800 text-white border-b-2 border-blue-500'
              : 'bg-gray-700 text-gray-300 hover:text-white'
          }`}
          onClick={() => setActiveTab('payoutQuery')}
        >
          Payout Query
        </button>

        <button
          className={`px-4 py-2 rounded-t-md text-sm font-medium transition-colors duration-300 ${
            activeTab === 'payoutQuery'
              ? 'bg-gray-800 text-white border-b-2 border-blue-500'
              : 'bg-gray-700 text-gray-300 hover:text-white'
          }`}
          onClick={() => setActiveTab('createAdmin')}
        >
          Create Admin
        </button>
      </div>

      {/* Tab content */}
      <div className="bg-gray-800 p-6 rounded-md shadow-md">
        {activeTab === 'balance' && <BalanceApi onShowModal={handleOpenModal} />}
        {activeTab === 'payin' && <PayinApi onSuccess={handlePayinSuccess} />}
        {activeTab === 'payinQuery' && <PayinQuery payinData={payinData} />}
        {activeTab === 'payout' && <PayoutApi payinData={payinData} />}
        {activeTab === 'payoutQuery' && <PayoutQuery payinData={payinData} />}
        {activeTab === 'createAdmin' && <CreateAdmin />}

      </div>

      {/* Modal Popup */}
      <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
        {modalContent}
      </Modal>
    </div>
  );
};

export default Home;
