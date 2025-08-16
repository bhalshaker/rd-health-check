# import required modules
import pytest
from unittest.mock import patch
from app.controller.tcp_based_connection import TcpBasedConnection

def test_establish_tcp_connection_success():
	# Mock socket.create_connection to simulate successful connection
	with patch('socket.create_connection', return_value=True) as mock_conn:
		result = TcpBasedConnection.establish_tcp_connection('127.0.0.1', 80)
		assert result is True
		mock_conn.assert_called_once_with(('127.0.0.1', 80), timeout=1)

def test_establish_tcp_connection_failure():
	# Mock socket.create_connection to raise an exception
	with patch('socket.create_connection', side_effect=Exception('Connection failed')) as mock_conn:
		result = TcpBasedConnection.establish_tcp_connection('127.0.0.1', 80)
		assert result is False
		mock_conn.assert_called_once_with(('127.0.0.1', 80), timeout=1)