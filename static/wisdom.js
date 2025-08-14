function deleteNote(noteId) {
    fetch('/delete-wisdom', {
        method: 'DELETE',
        headers: {
            'Context-Type': 'application/json'
        },
        body: JSON.stringify({ noteId: noteId})
    }).then((_res) => {
        window.location.href = "/post-wisdom";
    });
}