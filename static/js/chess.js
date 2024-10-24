document.addEventListener("DOMContentLoaded", function() {
    let draggedPiece = null;
    let startPos = null;
    let validMoves = [];

    // Make pieces draggable
    document.querySelectorAll('.piece').forEach(piece => {
        piece.draggable = true;
        piece.addEventListener('dragstart', handleDragStart);
        piece.addEventListener('click', handlePieceClick); // Allow click to highlight
    });

    const boardSquares = document.querySelectorAll('.square');
    boardSquares.forEach(square => {
        square.addEventListener('dragover', (e) => e.preventDefault()); // Allow dropping
        square.addEventListener('drop', handleDrop);
    });

    function handleDragStart(e) {
        draggedPiece = e.target;
        startPos = {
            row: e.target.closest('.square').dataset.row,
            col: e.target.closest('.square').dataset.col
        };

        // Fetch valid moves from the server
        fetch('/valid_moves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ start: startPos })
        })
        .then(response => response.json())
        .then(data => {
            validMoves = data.valid_moves;
            highlightValidMoves(validMoves);
        });
    }

    function handlePieceClick(e) {
        // Handle click highlighting
        startPos = {
            row: e.target.closest('.square').dataset.row,
            col: e.target.closest('.square').dataset.col
        };

        // Fetch valid moves for clicked piece
        fetch('/valid_moves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ start: startPos })
        })
        .then(response => response.json())
        .then(data => {
            validMoves = data.valid_moves;
            highlightValidMoves(validMoves);
        });
    }

    function handleDrop(e) {
        const targetSquare = e.target.closest('.square');
        const endPos = {
            row: targetSquare.dataset.row,
            col: targetSquare.dataset.col
        };

        if (!isValidMove(endPos)) {
            alert("Invalid move!");
            return;
        }

        // Move the piece visually
        targetSquare.innerHTML = '';
        targetSquare.appendChild(draggedPiece);

        // Send the move to the backend
        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ start: startPos, end: endPos })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  console.log('Move successful');
                  clearHighlights();
              } else {
                  alert(data.error || "Move failed");
              }
          });
    }

    function highlightValidMoves(validMoves) {
        clearHighlights();
        validMoves.forEach(move => {
            const square = document.querySelector(`[data-row='${move[0]}'][data-col='${move[1]}']`);
            if (square) {
                square.classList.add('highlight');
            }
        });
    }

    function clearHighlights() {
        document.querySelectorAll('.highlight').forEach(square => {
            square.classList.remove('highlight');
        });
    }

    function isValidMove(endPos) {
        return validMoves.some(move => move[0] == endPos.row && move[1] == endPos.col);
    }
});