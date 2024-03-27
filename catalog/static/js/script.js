function one() {
    if (this.classList.contains('collapsed')) {
        this.classList.remove('non-collapsed');
    } else {
        this.classList.add('non-collapsed');
    }
}