import React, { useState } from 'react';
import { useKeycloak } from '@react-keycloak/web';

interface Row {
  sensor_id: number;
  sensor_type: string;
  timestamp: string;
  value: number;
  product_id: number;
  product_type: string;
  person_id: number;
  last_name: string;
  first_name: string;
  patronymic: string;
  birthday: string;
  email: string;
}

const ReportPage: React.FC = () => {
  const { keycloak, initialized } = useKeycloak();
  const [loading, setLoading] = useState(false);
  const [reports, setReports] = useState<Row[]>([]);
  const [error, setError] = useState<string | null>(null);

  const downloadReport = async () => {
    if (!keycloak?.token) {
      setError('Not authenticated');
      return;
    }

    setLoading(true);
    setError(null);

    await fetch(`${process.env.REACT_APP_API_URL}/reports`, {
      headers: {
        'Authorization': `Bearer ${keycloak.token}`
      }
    })
        .then(async (response: Response) => {
          if (!response.ok) {
            throw new Error(await response.text() || `${response.status} ${response.statusText}`);
          }
          return response;
        })
        .then(res => res.json())
        .then(data => setReports(data))
        .catch(err => setError(err instanceof Error ? err.message : 'An error occurred'))
        .finally(() => setLoading(false));
  };

  if (!initialized) {
    return <div>Loading...</div>;
  }

  if (!keycloak.authenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <button
          onClick={() => keycloak.login()}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Login
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6">Usage Reports</h1>
        
        <button
          onClick={downloadReport}
          disabled={loading}
          className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ${
            loading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Generating Report...' : 'Download Report'}
        </button>

        {error && (
          <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}


        {reports.length > 0 && (
            <div className="mt-6 overflow-x-auto">
              <table className="min-w-full border border-gray-300">
                <thead>
                <tr className="bg-gray-200">
                  <th className="px-4 py-2 border">Id датчика</th>
                  <th className="px-4 py-2 border">Датчик</th>
                  <th className="px-4 py-2 border">Время события</th>
                  <th className="px-4 py-2 border">Значение</th>
                  <th className="px-4 py-2 border">Id изделия</th>
                  <th className="px-4 py-2 border">Изделие</th>
                  <th className="px-4 py-2 border">Id пользователя</th>
                  <th className="px-4 py-2 border">Фамилия</th>
                  <th className="px-4 py-2 border">Имя</th>
                  <th className="px-4 py-2 border">Отчество</th>
                  <th className="px-4 py-2 border">Дата рождения</th>
                  <th className="px-4 py-2 border">Email</th>
                </tr>
                </thead>
                <tbody>
                {reports.map((row, idx) => (
                    <tr key={idx} className="hover:bg-gray-100">
                      <td className="px-4 py-2 border">{row.sensor_id}</td>
                      <td className="px-4 py-2 border">{row.sensor_type}</td>
                      <td className="px-4 py-2 border">
                        {new Date(row.timestamp).toLocaleString()}
                      </td>
                      <td className="px-4 py-2 border">{row.value}</td>
                      <td className="px-4 py-2 border">{row.product_id}</td>
                      <td className="px-4 py-2 border">{row.product_type}</td>
                      <td className="px-4 py-2 border">{row.person_id}</td>
                      <td className="px-4 py-2 border">{row.last_name}</td>
                      <td className="px-4 py-2 border">{row.first_name}</td>
                      <td className="px-4 py-2 border">{row.patronymic}</td>
                      <td className="px-4 py-2 border">{row.birthday}</td>
                      <td className="px-4 py-2 border">{row.email}</td>
                    </tr>
                ))}
                </tbody>
              </table>
            </div>
        )}
      </div>
    </div>
  );
};

export default ReportPage;