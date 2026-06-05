from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Ensure project root is in path for imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize RAG Engine
try:
    from engine import RAGEngine
    engine = RAGEngine()
except Exception as e:
    print(f"Warning: Could not load RAG Engine: {e}")
    engine = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'engine': 'available' if engine else 'unavailable'
    })

@app.route('/api/query', methods=['POST'])
def query_endpoint():
    """Main query endpoint"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        fund_filter = data.get('fund', None)
        debug = data.get('debug', False)
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400
        
        if not engine:
            return jsonify({
                'success': False,
                'error': 'Engine not initialized'
            }), 503
        
        # Query the engine
        response = engine.query(question, filter_fund=fund_filter)
        
        result = {
            'success': True,
            'answer': response,
            'fund': fund_filter or 'all',
            'debug': {
                'question': question,
                'timestamp': str(__import__('datetime').datetime.now()),
                'debug_mode': debug
            } if debug else None
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/funds', methods=['GET'])
def get_funds():
    """Get available funds"""
    try:
        if engine:
            funds = engine.get_available_funds()
            return jsonify({
                'success': True,
                'funds': funds
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Engine not available'
            }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Chat endpoint with message history support"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        history = data.get('history', [])
        fund_filter = data.get('fund', None)
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        if not engine:
            return jsonify({
                'success': False,
                'error': 'Engine not initialized'
            }), 503
        
        # For now, just query with the current message
        # In future, you can implement context-aware responses with history
        response = engine.query(message, filter_fund=fund_filter)
        
        return jsonify({
            'success': True,
            'response': response,
            'message_id': len(history),
            'fund': fund_filter or 'all'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
