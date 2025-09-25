import React, { useState } from 'react';

interface FeedbackModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (feedback: { feedback_text: string; rating: number }) => void;
}

export const FeedbackModal: React.FC<FeedbackModalProps> = ({
  isOpen,
  onClose,
  onSubmit
}) => {
  const [feedbackText, setFeedbackText] = useState('');
  const [rating, setRating] = useState(3);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!feedbackText.trim()) {
      alert('Please provide feedback text');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({ feedback_text: feedbackText, rating });
      setFeedbackText('');
      setRating(3);  
      setHoveredRating(0);
      onClose();
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Error sending feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getRatingText = (currentRating: number) => {
    switch(currentRating) {
      case 1: return 'Poor';
      case 2: return 'Fair';
      case 3: return 'Good';
      case 4: return 'Very Good';
      case 5: return 'Excellent';
      default: return 'Good';
    }
  };

  return (
    <div 
      style={{ 
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.7)',
        backdropFilter: 'blur(4px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        padding: '16px'
      }}
    >
      <div 
        style={{
          background: 'var(--panel)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          width: '100%',
          maxWidth: '480px',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4)',
          color: 'var(--text)',
          transform: isOpen ? 'scale(1)' : 'scale(0.95)',
          transition: 'transform 0.2s ease'
        }}
      >
        {/* Header con X en la esquina */}
        <div style={{ 
          padding: '20px 24px 16px', 
          borderBottom: '1px solid var(--border)',
          position: 'relative'
        }}>
          <button 
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '16px',
              right: '20px',
              background: 'none',
              border: 'none',
              color: 'var(--muted)',
              fontSize: '20px',
              cursor: 'pointer',
              padding: '4px',
              borderRadius: '6px',
              lineHeight: 1
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'var(--border)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
          >
            ✕
          </button>
          
          <div style={{ paddingRight: '40px' }}>
            <div style={{ fontSize: '20px', marginBottom: '8px' }}>
              😔 Help us improve
            </div>
            <div style={{ 
              color: 'var(--muted)', 
              fontSize: '14px',
              lineHeight: '1.4'
            }}>
              We noticed you might be frustrated. Your feedback helps us get better.
            </div>
          </div>
        </div>

        {/* Contenido del modal */}
        <form onSubmit={handleSubmit} style={{ padding: '24px' }}>
          
          {/* Rating mejorado con hover */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ 
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: 'var(--text)',
              marginBottom: '12px'
            }}>
              Rate your experience:
            </label>
            
            <div style={{ 
              display: 'flex', 
              gap: '4px', 
              justifyContent: 'center',
              marginBottom: '8px'
            }}>
              {[1, 2, 3, 4, 5].map((star) => {
                const isActive = star <= (hoveredRating || rating);
                return (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    onMouseEnter={() => setHoveredRating(star)}
                    onMouseLeave={() => setHoveredRating(0)}
                    style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '28px',
                      cursor: 'pointer',
                      padding: '4px',
                      borderRadius: '4px',
                      transition: 'all 0.15s ease',
                      color: isActive ? '#facc15' : 'var(--border)'
                    }}
                  >
                    ★
                  </button>
                );
              })}
            </div>
            
            <p style={{ 
              textAlign: 'center',
              fontSize: '13px',
              color: 'var(--muted)',
              margin: 0
            }}>
              {getRatingText(hoveredRating || rating)}
            </p>
          </div>

          {/* Textarea mejorado */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ 
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: 'var(--text)',
              marginBottom: '8px'
            }}>
              What frustrated you?
            </label>
            <textarea
              value={feedbackText}
              onChange={(e) => setFeedbackText(e.target.value)}
              placeholder="Tell us what happened and how we can improve..."
              style={{
                width: '100%',
                padding: '12px 14px',
                background: '#0f1424',
                color: 'var(--text)',
                border: '1px solid var(--border)',
                borderRadius: '10px',
                resize: 'none',
                lineHeight: '1.4',
                fontSize: '14px',
                fontFamily: 'inherit',
                minHeight: '80px',
                outline: 'none',
                transition: 'border-color 0.15s ease'
              }}
              onFocus={(e) => e.target.style.borderColor = 'var(--accent)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--border)'}
              rows={3}
              required
            />
          </div>

          {/* Botones mejorados */}
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                flex: 1,
                padding: '12px 16px',
                background: 'transparent',
                color: 'var(--muted)',
                border: '1px solid var(--border)',
                borderRadius: '10px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '500',
                transition: 'all 0.15s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'var(--border)';
                e.currentTarget.style.color = 'var(--text)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = 'var(--muted)';
              }}
            >
              Skip
            </button>
            
            <button
              type="submit"
              disabled={isSubmitting || !feedbackText.trim()}
              style={{
                flex: 1,
                padding: '12px 16px',
                background: isSubmitting || !feedbackText.trim() ? 'var(--border)' : 'var(--accent)',
                color: isSubmitting || !feedbackText.trim() ? 'var(--muted)' : '#0b1020',
                border: '1px solid var(--border)',
                borderRadius: '10px',
                cursor: isSubmitting || !feedbackText.trim() ? 'not-allowed' : 'pointer',
                fontSize: '14px',
                fontWeight: '600',
                transition: 'all 0.15s ease'
              }}
              onMouseEnter={(e) => {
                if (!isSubmitting && feedbackText.trim()) {
                  e.currentTarget.style.transform = 'translateY(-1px)';
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(110, 231, 183, 0.3)';
                }
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {isSubmitting ? 'Sending...' : 'Send Feedback'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};