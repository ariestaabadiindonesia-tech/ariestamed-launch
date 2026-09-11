import React, { useEffect, useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import useAuthStore from '../store/authStore';
import api from '../services/api';

const DashboardPage = () => {
    const { user } = useAuthStore();
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchDashboardStats();
    }, []);

    const fetchDashboardStats = async () => {
        try {
            setLoading(true);
            const response = await api.get('/analytics/dashboard');
            setStats(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to load dashboard');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;
    if (error) return <div className="text-red-500 p-4">{error}</div>;

    const platformData = stats?.platforms ? Object.entries(stats.platforms).map(([name, data]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        posts: data.posts,
        views: data.views,
        engagement: data.engagement
    })) : [];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-800">Welcome back, {user?.full_name || user?.username}! 👋</h1>
                    <p className="text-gray-600 mt-2">Here's your social media performance overview</p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <StatCard title="Total Posts" value={stats?.total_posts || 0} icon="📝" />
                    <StatCard title="Published" value={stats?.published_posts || 0} icon="✅" />
                    <StatCard title="Scheduled" value={stats?.scheduled_posts || 0} icon="📅" />
                    <StatCard title="Total Views" value={(stats?.total_views || 0).toLocaleString()} icon="👁️" />
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Platform Performance */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-bold mb-4">Platform Performance</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={platformData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="posts" fill="#3b82f6" />
                                <Bar dataKey="engagement" fill="#10b981" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Engagement Trend */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-bold mb-4">Engagement Overview</h2>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                                <span className="font-semibold">Total Engagement</span>
                                <span className="text-2xl font-bold text-blue-600">{stats?.total_engagement?.toLocaleString() || 0}</span>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                {platformData.map((platform) => (
                                    <div key={platform.name} className="p-3 bg-gradient-to-br from-purple-50 to-pink-50 rounded">
                                        <p className="text-sm text-gray-600">{platform.name}</p>
                                        <p className="text-xl font-bold text-purple-600">{platform.engagement}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <QuickActionButton icon="✏️" label="Create Content" link="/content" />
                        <QuickActionButton icon="📅" label="Schedule Post" link="/posts" />
                        <QuickActionButton icon="📊" label="View Analytics" link="/analytics" />
                        <QuickActionButton icon="🏢" label="Manage Products" link="/products" />
                    </div>
                </div>
            </div>
        </div>
    );
};

const StatCard = ({ title, value, icon }) => (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
        <div className="flex justify-between items-start">
            <div>
                <p className="text-gray-600 text-sm font-semibold">{title}</p>
                <p className="text-3xl font-bold text-gray-800 mt-2">{value}</p>
            </div>
            <span className="text-4xl">{icon}</span>
        </div>
    </div>
);

const QuickActionButton = ({ icon, label, link }) => (
    <a href={link} className="p-4 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg text-white hover:shadow-lg transition text-center font-semibold">
        <div className="text-3xl mb-2">{icon}</div>
        <div>{label}</div>
    </a>
);

export default DashboardPage;
