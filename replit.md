# FitTracker - Workout Planner & Tracker

## Overview

FitTracker is a Progressive Web Application (PWA) designed for fitness enthusiasts to plan, track, and monitor their workout routines. The application provides a comprehensive platform for creating custom workout plans, tracking exercise sessions in real-time, and analyzing fitness progress over time. Built as a PWA, it offers offline functionality and can be installed on mobile devices for a native app-like experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Progressive Web App (PWA)**: Implements service worker for offline functionality and caching strategies
- **Bootstrap Framework**: Uses Bootstrap 5 with dark theme for responsive UI design
- **Vanilla JavaScript**: Client-side functionality handled through modular JavaScript classes
- **Chart.js**: Integrated for progress visualization and workout analytics
- **Feather Icons**: Lightweight icon system for consistent UI elements

### Backend Architecture
- **Flask Framework**: Python web framework handling routing and server-side logic
- **Blueprint Pattern**: Organized code structure with separate blueprints for authentication and main routes
- **Flask-Login**: Session management and user authentication handling
- **In-Memory Storage**: Temporary data storage using Python dictionaries for rapid prototyping

### Authentication System
- **Google OAuth 2.0**: Primary authentication method using Google's OAuth service
- **Flask-Login Integration**: User session management with secure login/logout functionality
- **User Model**: Custom User class implementing Flask-Login's UserMixin for session handling

### Data Models
- **User Model**: Handles user authentication, profile data, and session management
- **WorkoutPlan Model**: Manages workout plan creation with exercise selection and configuration
- **WorkoutSession Model**: Tracks active workout sessions with timing and progress data
- **Exercise Library**: Predefined exercise database with muscle groups, equipment, and descriptions

### Workout Tracking Features
- **Real-time Timer**: JavaScript-based workout and rest timers for session tracking
- **Progress Persistence**: Local storage for workout progress backup during sessions
- **Set/Rep Tracking**: Detailed logging of exercise performance with weight and repetition data
- **Session Analytics**: Progress charts and statistics for workout frequency and improvement tracking

### PWA Implementation
- **Service Worker**: Caches static assets and pages for offline functionality
- **Web App Manifest**: Defines PWA metadata, icons, and installation behavior
- **Responsive Design**: Mobile-first approach with touch-optimized interface
- **Offline Support**: Core functionality available without internet connection

## External Dependencies

### Authentication Services
- **Google OAuth 2.0 API**: Handles user authentication and profile data retrieval
- **Google Discovery Document**: Dynamic OAuth endpoint configuration

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework via CDN for responsive design
- **Chart.js**: Data visualization library for progress charts and analytics
- **Feather Icons**: Icon library for consistent UI elements
- **Bootstrap Bundle**: JavaScript components for interactive UI elements

### Python Dependencies
- **Flask**: Core web framework for backend development
- **Flask-Login**: User session management and authentication
- **Flask-CORS**: Cross-origin resource sharing for PWA functionality
- **OAuthLib**: OAuth 2.0 client implementation for Google authentication
- **Requests**: HTTP client for external API communication

### Development Environment
- **Replit Platform**: Cloud-based development environment with automatic SSL
- **Environment Variables**: Secure storage for OAuth credentials and session secrets
- **Debug Mode**: Development configuration with detailed error logging

## GitHub Repository Setup

**Note**: GitHub integration requires manual setup due to Replit's git restrictions.

To create a GitHub repository and push this code:

1. **Create Repository on GitHub**:
   - Go to https://github.com/new
   - Repository name: `fittracker-pwa`
   - Description: `Progressive Web App for workout planning and tracking with offline capabilities`
   - Make it public
   - Click "Create repository"

2. **Connect and Push from Replit**:
   - Open the Shell in Replit
   - Run these commands:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/fittracker-pwa.git
   git add .
   git commit -m "Initial commit: FitTracker PWA with workout planning and tracking"
   git branch -M main
   git push -u origin main
   ```

3. **Repository Features**:
   - Issues tracking enabled
   - Wiki documentation available
   - Project boards for task management