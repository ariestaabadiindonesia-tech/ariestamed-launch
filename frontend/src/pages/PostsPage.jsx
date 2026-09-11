import React, { useEffect, useState } from 'react';
import api from '../services/api';

const PostsPage = () => {
    const [posts, setPosts] = useState([]);
    const [products, setProducts] = useState([]);
    const [contents, setContents] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [showScheduler, setShowScheduler] = useState(false);
    const [formData, setFormData] = useState({
        content_id: '',
        platform: 'instagram',
        scheduled_at: new Date().toISOString().slice(0, 16)
    });

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setIsLoading(true);
            const [postsRes, contentsRes] = await Promise.all([
                api.get('/posts'),
                api.get('/content')
            ]);
            setPosts(postsRes.data.posts);
            setContents(contentsRes.data.contents);
        } catch (error) {
            console.error('Failed to fetch data', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSchedulePost = async () => {
        if (!formData.content_id) {
            alert('Please select content');
            return;
        }
        try {
            await api.post('/posts', formData);
            alert('Post scheduled successfully!');
            setShowScheduler(false);
            setFormData({
                content_id: '',
                platform: 'instagram',
                scheduled_at: new Date().toISOString().slice(0, 16)
            });
            fetchData();
        } catch (error) {
            alert('Failed to schedule post: ' + error.response?.data?.error);
        }
    };

    const handlePublishPost = async (postId) => {
        try {
            await api.post(`/posts/${postId}/publish`);
            alert('Post published!');
            fetchData();
        } catch (error) {
            alert('Failed to publish post: ' + error.response?.data?.error);
        }
    };

    const handleCancelPost = async (postId) => {
        if (window.confirm('Cancel this post?')) {
            try {
                await api.post(`/posts/${postId}/cancel`);
                alert('Post cancelled');
                fetchData();
            } catch (error) {
                alert('Failed to cancel post');
            }
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-100 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-800">📅 Post Scheduler</h1>
                        <p className="text-gray-600 mt-2">Schedule and manage your social media posts</p>
                    </div>
                    <button
                        onClick={() => setShowScheduler(true)}
                        className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 px-6 rounded-lg transition"
                    >
                        + Schedule Post
                    </button>
                </div>

                {/* Scheduler Modal */}
                {showScheduler && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
                            <h2 className="text-2xl font-bold mb-4">📅 Schedule Post</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Select Content *</label>
                                    <select
                                        value={formData.content_id}
                                        onChange={(e) => setFormData({ ...formData, content_id: e.target.value })}
                                        className="w-full border rounded-lg p-2"
                                    >
                                        <option value="">Choose content...</option>
                                        {contents.filter(c => c.status === 'approved').map((c) => (
                                            <option key={c.id} value={c.id}>
                                                {c.title} - {c.platform}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Platform</label>
                                    <select
                                        value={formData.platform}
                                        onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                                        className="w-full border rounded-lg p-2"
                                    >
                                        <option value="instagram">Instagram</option>
                                        <option value="facebook">Facebook</option>
                                        <option value="tiktok">TikTok</option>
                                        <option value="youtube">YouTube</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Schedule Time</label>
                                    <input
                                        type="datetime-local"
                                        value={formData.scheduled_at}
                                        onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value })}
                                        className="w-full border rounded-lg p-2"
                                    />
                                </div>
                                <div className="flex gap-2 pt-4">
                                    <button
                                        onClick={handleSchedulePost}
                                        className="flex-1 bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 rounded transition"
                                    >
                                        Schedule
                                    </button>
                                    <button
                                        onClick={() => setShowScheduler(false)}
                                        className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 rounded transition"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Posts List */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-2xl font-bold mb-6">Posts Timeline</h2>
                    {isLoading ? (
                        <p className="text-center py-8">Loading posts...</p>
                    ) : posts.length === 0 ? (
                        <p className="text-center py-8 text-gray-600">No posts yet. Schedule your first one!</p>
                    ) : (
                        <div className="space-y-4">
                            {posts.map((post) => (
                                <div key={post.id} className="border rounded-lg p-4 hover:bg-gray-50 transition">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <div className="flex gap-2 mb-2">
                                                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                                    post.status === 'draft' ? 'bg-gray-200 text-gray-800' :
                                                    post.status === 'scheduled' ? 'bg-yellow-200 text-yellow-800' :
                                                    post.status === 'published' ? 'bg-green-200 text-green-800' :
                                                    'bg-red-200 text-red-800'
                                                }`}>
                                                    {post.status.toUpperCase()}
                                                </span>
                                                <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold">
                                                    {post.platform.toUpperCase()}
                                                </span>
                                            </div>
                                            <p className="text-gray-600 text-sm">
                                                Scheduled for: {new Date(post.scheduled_at).toLocaleString()}
                                            </p>
                                        </div>
                                        {post.status === 'scheduled' && (
                                            <div className="flex gap-2">
                                                <button
                                                    onClick={() => handlePublishPost(post.id)}
                                                    className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
                                                >
                                                    Publish Now
                                                </button>
                                                <button
                                                    onClick={() => handleCancelPost(post.id)}
                                                    className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
                                                >
                                                    Cancel
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PostsPage;
