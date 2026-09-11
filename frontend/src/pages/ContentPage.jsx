import React, { useEffect, useState } from 'react';
import useContentStore from '../store/contentStore';
import useProductStore from '../store/productStore';

const ContentPage = () => {
    const { contents, fetchContents, generateContent, createContent, updateContent, isLoading } = useContentStore();
    const { products } = useProductStore();
    const [showForm, setShowForm] = useState(false);
    const [showGenerator, setShowGenerator] = useState(false);
    const [formData, setFormData] = useState({
        product_id: '',
        title: '',
        text: '',
        content_type: 'caption',
        platform: 'instagram',
        hashtags: [],
        call_to_action: ''
    });
    const [generatorData, setGeneratorData] = useState({
        product_id: '',
        content_type: 'caption',
        platform: 'instagram',
        tone: 'professional',
        length: 'medium'
    });

    useEffect(() => {
        fetchContents();
    }, []);

    const handleGenerateContent = async () => {
        if (!generatorData.product_id) {
            alert('Please select a product');
            return;
        }
        const result = await generateContent(generatorData);
        if (result) {
            alert('Content generation started! Check back in a moment.');
            setShowGenerator(false);
            setTimeout(() => fetchContents(), 3000);
        }
    };

    const handleCreateContent = async () => {
        if (!formData.product_id || !formData.text) {
            alert('Please fill in all required fields');
            return;
        }
        await createContent(formData);
        setShowForm(false);
        setFormData({
            product_id: '',
            title: '',
            text: '',
            content_type: 'caption',
            platform: 'instagram',
            hashtags: [],
            call_to_action: ''
        });
        fetchContents();
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-800">✨ Content Management</h1>
                        <p className="text-gray-600 mt-2">Create and manage your social media content</p>
                    </div>
                    <div className="flex gap-4">
                        <button
                            onClick={() => setShowGenerator(true)}
                            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition"
                        >
                            🤖 AI Generate
                        </button>
                        <button
                            onClick={() => setShowForm(true)}
                            className="bg-pink-600 hover:bg-pink-700 text-white font-bold py-3 px-6 rounded-lg transition"
                        >
                            + Create Manual
                        </button>
                    </div>
                </div>

                {/* AI Generator Modal */}
                {showGenerator && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
                            <h2 className="text-2xl font-bold mb-4">🤖 Generate Content with AI</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Product *</label>
                                    <select
                                        value={generatorData.product_id}
                                        onChange={(e) => setGeneratorData({ ...generatorData, product_id: e.target.value })}
                                        className="w-full border rounded-lg p-2"
                                    >
                                        <option value="">Select a product</option>
                                        {products.map((p) => (
                                            <option key={p.id} value={p.id}>
                                                {p.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Content Type</label>
                                    <select
                                        value={generatorData.content_type}
                                        onChange={(e) => setGeneratorData({ ...generatorData, content_type: e.target.value })}
                                        className="w-full border rounded-lg p-2"
                                    >
                                        <option value="caption">Caption</option>
                                        <option value="post">Post</option>
                                        <option value="story">Story</option>
                                        <option value="video_desc">Video Description</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-2">Platform</label>
                                    <select
                                        value={generatorData.platform}
                                        onChange={(e) => setGeneratorData({ ...generatorData, platform: e.target.value })}
                                        className="w-full border rounded-lg p-2"
                                    >
                                        <option value="instagram">Instagram</option>
                                        <option value="facebook">Facebook</option>
                                        <option value="tiktok">TikTok</option>
                                        <option value="youtube">YouTube</option>
                                    </select>
                                </div>
                                <div className="flex gap-2 pt-4">
                                    <button
                                        onClick={handleGenerateContent}
                                        className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 rounded transition"
                                    >
                                        Generate
                                    </button>
                                    <button
                                        onClick={() => setShowGenerator(false)}
                                        className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 rounded transition"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Contents List */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-2xl font-bold mb-6">Your Content</h2>
                    {isLoading ? (
                        <p className="text-center py-8">Loading content...</p>
                    ) : contents.length === 0 ? (
                        <p className="text-center py-8 text-gray-600">No content yet. Create your first one!</p>
                    ) : (
                        <div className="space-y-4">
                            {contents.map((content) => (
                                <div key={content.id} className="border rounded-lg p-4 hover:bg-gray-50 transition">
                                    <div className="flex justify-between items-start mb-2">
                                        <div>
                                            <h3 className="font-bold text-lg">{content.title}</h3>
                                            <p className="text-gray-600 text-sm line-clamp-2">{content.text}</p>
                                        </div>
                                        <div className="flex gap-2">
                                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                                content.status === 'draft' ? 'bg-gray-200 text-gray-800' :
                                                content.status === 'approved' ? 'bg-green-200 text-green-800' :
                                                'bg-blue-200 text-blue-800'
                                            }`}>
                                                {content.status}
                                            </span>
                                            <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold">
                                                {content.platform}
                                            </span>
                                        </div>
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

export default ContentPage;
