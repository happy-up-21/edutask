// src/pages/HomePage.tsx
import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { AuthCard } from '../components/AuthCard';

export const HomePage: React.FC = () => {
    const { user, loading, error, loginWithGoogle, logout } = useAuth();

    return (
        <AuthCard
            user={user}
            loading={loading}
            error={error}
            onLogin={loginWithGoogle}
            onLogout={logout}
        />
    );
};
