import create from 'zustand';
import api from './api';

const useContentStore = create((set) => ({
    contents: [],
    currentContent: null,
    isLoading: false,
    error: null,

    fetchContents: async (filters = {}) => {
        set({ isLoading: true, error: null });
        try {
            const params = new URLSearchParams(filters);
            const response = await api.get(`/content?${params}`);
            set({ contents: response.data.contents, isLoading: false });
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to fetch content', isLoading: false });
        }
    },

    generateContent: async (generationParams) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/content/generate', generationParams);
            return response.data;
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to generate content', isLoading: false });
        }
    },

    createContent: async (contentData) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/content', contentData);
            set((state) => ({
                contents: [...state.contents, response.data.content],
                isLoading: false,
            }));
            return response.data;
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to create content', isLoading: false });
        }
    },

    updateContent: async (id, contentData) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.put(`/content/${id}`, contentData);
            set((state) => ({
                contents: state.contents.map((c) => (c.id === id ? response.data.content : c)),
                isLoading: false,
            }));
            return response.data;
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to update content', isLoading: false });
        }
    },

    approveContent: async (id) => {
        try {
            const response = await api.put(`/content/${id}/approve`);
            set((state) => ({
                contents: state.contents.map((c) => (c.id === id ? response.data.content : c)),
            }));
            return response.data;
        } catch (error) {
            console.error('Failed to approve content', error);
        }
    },
}));

export default useContentStore;
