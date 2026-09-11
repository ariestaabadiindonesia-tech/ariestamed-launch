import React, { useEffect, useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../services/api';

const AnalyticsPage = () => {
    const [dashboardStats, setDashboardStats] = useState(null);
    const [selectedPlatform, setSelectedPlatform] = useState('instagram');
    const [platformStats, setPlatformStats] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [startDate, setStartDate] = useState(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]);
    const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0]);

    useEffect(() => {
        fetchAnalytics();
    }, [selectedPlatform, startDate, endDate]);

    const fetchAnalytics = async () => {
        try {
            setIsLoading(true);
            const [dashRes, platRes] = await Promise.all([
                api.get('/analytics/dashboard'),
                api.get(`/analytics/platform/${selectedPlatform}`)
            ]);
            setDashboardStats(dashRes.data);
            setPlatformStats(platRes.data);
        } catch (error) {
            console.error('Failed to fetch analytics', error);
        } finally {
            setIsLoading(false);
        }
    };

    if (!dashboardStats || !platformStats) return <div className="flex justify-center items-center h-screen">Loading...</div>;

    const platformsData = dashboardStats.platforms ? Object.entries(dashboardStats.platforms).map(([name, data]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        posts: data.posts,
        views: data.views,
        engagement: data.engagement
    })) : [];

    return (
        <div className="min-h-screen bg-gradient-to-br from-cyan-50 to-blue-100 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-800">📊 Analytics Dashboard</h1>
                    <p className="text-gray-600 mt-2">Track your social media performance</p>
                </div>

                {/* Date Range Filter */}
                <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <div className="flex gap-4 items-end">
                        <div>
                            <label className="block text-sm font-semibold mb-2">Start Date</label>
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className="border rounded-lg p-2"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-semibold mb-2">End Date</label>
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="border rounded-lg p-2"
                            />
                        </div>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
                            Apply
                        </button>
                    </div>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <MetricCard title="Total Views" value={(dashboardStats.total_views || 0).toLocaleString()} icon="👁️" />
                    <MetricCard title="Total Engagement" value={(dashboardStats.total_engagement || 0).toLocaleString()} icon="💬" />
                    <MetricCard title="Published Posts" value={dashboardStats.published_posts || 0} icon="✅" />
                    <MetricCard title="Avg. Engagement Rate" value={`${(dashboardStats.total_engagement / (dashboardStats.total_views || 1) * 100).toFixed(2)}%`} icon="📈" />
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Platform Comparison */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-bold mb-4">Platform Comparison</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={platformsData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="views" fill="#3b82f6" />
                                <Bar dataKey="engagement" fill="#10b981" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Platform Stats */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-bold mb-4">Selected Platform Stats</h2>
                        <select
                            value={selectedPlatform}
                            onChange={(e) => setSelectedPlatform(e.target.value)}
                            className="w-full border rounded-lg p-2 mb-4"
                        >
                            <option value="instagram">Instagram</option>
                            <option value="facebook">Facebook</option>
                            <option value="tiktok">TikTok</option>
                            <option value="youtube">YouTube</option>
                        </select>
                        <div className="space-y-3">
                            <div className="flex justify-between p-3 bg-blue-50 rounded">
                                <span>Views</span>
                                <span className="font-bold text-blue-600">{(platformStats.total_views || 0).toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between p-3 bg-green-50 rounded">
                                <span>Engagement</span>
                                <span className="font-bold text-green-600">{(platformStats.total_engagement || 0).toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between p-3 bg-purple-50 rounded">
                                <span>Posts</span>
                                <span className="font-bold text-purple-600">{platformStats.post_count || 0}</span>
                            </div>
                            <div className="flex justify-between p-3 bg-orange-50 rounded">
                                <span>Avg. Engagement Rate</span>
                                <span className="font-bold text-orange-600">{(platformStats.average_engagement_rate || 0).toFixed(2)}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const MetricCard = ({ title, value, icon }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start">
            <div>
                <p className="text-gray-600 text-sm font-semibold">{title}</p>
                <p className="text-3xl font-bold text-gray-800 mt-2">{value}</p>
            </div>
            <span className="text-4xl">{icon}</span>
        </div>
    </div>
);

export default AnalyticsPage;
