import create from 'zustand';
import api from './api';

const useAuthStore = create((set) => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isLoading: false,
    error: null,

    login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/auth/login', { email, password });
            const { access_token, user } = response.data;
            localStorage.setItem('access_token', access_token);
            set({ token: access_token, user, isLoading: false });
        } catch (error) {
            set({ error: error.response?.data?.error || 'Login failed', isLoading: false });
        }
    },

    register: async (username, email, password, fullName) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/auth/register', {
                username,
                email,
                password,
                full_name: fullName,
            });
            set({ isLoading: false });
            return response.data;
        } catch (error) {
            set({ error: error.response?.data?.error || 'Registration failed', isLoading: false });
        }
    },

    logout: () => {
        localStorage.removeItem('access_token');
        set({ token: null, user: null });
    },

    getProfile: async () => {
        try {
            const response = await api.get('/auth/profile');
            set({ user: response.data });
        } catch (error) {
            console.error('Failed to get profile', error);
        }
    },
}));

export default useAuthStore;
