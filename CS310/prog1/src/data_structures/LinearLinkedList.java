package data_structures;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * William Fox cssc0917
 * LinearLinkedList
 */
public class LinearLinkedList<E> implements LinearListADT<E> {
    private Node<E> head;
    private Node<E> tail;
    private int size;

    public LinearLinkedList() {
        head = tail = null;
        size = 0;
    }

    public void addLast(E obj) {
        Node<E> newNode = new Node<E>(obj);
        if (isEmpty())
            head = tail = newNode;
        else {
            tail.next = newNode;
            tail = newNode;
        }
        size++;
    }

    public void addFirst(E obj) {
        Node<E> newNode = new Node<E>(obj);
        if (isEmpty())
            head = tail = newNode;
        else {
            newNode.next = head;
            head = newNode;
        }
        size++;
    }

    public void insert(E obj, int location) {
        if (!isValidInsertLocation(location))
            throw new RuntimeException("List elements must be contiguous");
        if (location == 1) {
            addFirst(obj);
        } else if (location == size + 1) {
            addLast(obj);
        } else {
            Node<E> newNode = new Node<E>(obj);
            Node<E> tempNode = head;
            for (int i = 1; i < location - 1; i++) {
                tempNode = tempNode.next;
            }
            newNode.next = tempNode.next;
            tempNode.next = newNode;
            size++;
        }
    }

    public E remove(int location) {
        if (!isValidRemoveLocation(location))
            throw new RuntimeException("Location does not map to a valid position within the list");
        Node<E> previous = null;
        Node<E> current = head;
        E temp;
        for (int i = 0; i < location - 1; i++) {
            previous = current;
            current = current.next;
        }
        if (current == null)
            return null;
        if (current == head) {
            temp = current.data;
            head = head.next;
        } else if (current == tail) {
            temp = current.data;
            previous.next = null;
            tail = previous;
        } else {
            temp = current.data;
            previous.next = current.next;
        }
        if (head == null)
            tail = null;
        size--;
        return temp;
    }

    public E remove(E obj) {
        Node<E> previous = null;
        Node<E> current = head;
        E data;
        while (current != null && ((Comparable<E>) obj).compareTo(current.data) != 0) {
            previous = current;
            current = current.next;
        }
        if (current == null)
            return null;
        if (current == head) {
            data = current.data;
            head = head.next;
        } else if (current == tail) {
            data = current.data;
            previous.next = null;
            tail = previous;
        } else {
            data = current.data;
            previous.next = current.next;
        }
        if (head == null)
            tail = null;
        size--;
        return data;
    }

    public E removeFirst() {
        if (isEmpty())
            return null;
        E temp = head.data;
        head = head.next;
        size--;
        return temp;
    }

    public E removeLast() {
        if (isEmpty())
            return null;
        return remove(size);
    }

    public E get(int location) {
        if (!isValidRemoveLocation(location))
            throw new RuntimeException("Location does not map to a valid position within the list");
        Node<E> tempNode = head;
        for (int i = 1; i < location; i++) {
            tempNode = tempNode.next;
        }
        return tempNode.data;
    }

    public boolean isEmpty() {
        return size == 0;
    }
    public boolean contains(E obj) {
        return (!(locate(obj) == -1));
    }

    public int locate(E obj) {
        Node<E> tempNode = head;
        int location = 1;
        while (tempNode != null) {
            if (((Comparable<E>) obj).compareTo(tempNode.data) == 0)
                return location;
            tempNode = tempNode.next;
            location++;
        }
        return -1;
    }

    public void clear() {
        head = tail = null;
        size = 0;
    }

    public int size() {
        return size;
    }

    public Iterator<E> iterator() {
        return new IteratorHelper();
    }

    private class IteratorHelper implements Iterator<E> {
            private Node<E> tempNode;

            public IteratorHelper() {
                tempNode = head;
            }

            public boolean hasNext() {
                return ((tempNode != null));// && (tempNode.next != null));
            }

            public E next() {
                if (!hasNext()) throw new NoSuchElementException();
                E temp = tempNode.data;
                tempNode = tempNode.next;
                return temp;
            }

            public void remove() {
                throw new UnsupportedOperationException();
            }
        }

        private class Node<E> {
            public E data;
            public Node<E> next;

            public Node(E obj) {
                data = obj;
                next = null;
            }

    }

    private boolean isValidRemoveLocation(int location) {
        return ((location >= 1) && (location <= size));
    }
    private boolean isValidInsertLocation(int location) {
        return ((location >= 1) && (location - 1 <= size));
    }

}//Eof
