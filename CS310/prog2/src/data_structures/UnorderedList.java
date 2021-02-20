package data_structures;

import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * William Fox cssc0917
 * Prog2, Priority Queue, UnorderedList
 */
public class UnorderedList<E extends Comparable<E>> implements Iterable<E> {
    private Node<E> head, tail;
    int size;
    private long modificationCounter;

    public UnorderedList() {
        head = tail = null;
        modificationCounter = size = 0;
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
        modificationCounter++;
    }
    public void addFirst(E obj) {
        Node<E> newNode = new Node<E>(obj);
        if (isEmpty())
            head = tail = newNode;
        else {
            newNode.next = head.next;
            head = newNode;
        }
        size++;
        modificationCounter++;
    }
    public E removeFirst() {
        if (isEmpty())
            return null;
        E data = head.data;
        head = head.next;
        size--;
        modificationCounter++;
        return data;
    }
    public E findMin() {
        if (isEmpty())
            return null;
        Node<E> current;
        E min;
        current = head;
        min = current.data;
        while (current != null) {
            if (current.data.compareTo(min) < 0)
                min = current.data;
            current = current.next;
        }
        return min;
    }
    public E removeMin() {
        if (isEmpty())
            return null;
        Node<E> previous, current, min, minPrevious;
        min = current = head;
        previous = minPrevious = null;
        while (current != null) {
            if (current.data.compareTo(min.data) < 0) {
                min = current;
                minPrevious = previous;
            }
            previous = current;
            current = current.next;
        }
        previous = minPrevious;
        current = min;
        if (current == head) {
            head = head.next;
        } else if (current == tail) {
            previous.next = null;
            tail = previous;
        } else {
            previous.next = current.next;
        }
        if (head == null)
            tail = null;
        size--;
        modificationCounter++;
        return min.data;
    }
    public int size() {
        return size;
    }
    public boolean isEmpty() {
        return head == null;
    }

    public void clear() {
        head = tail = null;
        modificationCounter++;
        size = 0;
    }
    public boolean contains(E obj) {
        Node<E> pointer = head;
        while (pointer != null) {
            if (obj.compareTo(pointer.data) == 0)
                return true;
            pointer = pointer.next;
        }
        return false;
    }
    public Iterator<E> iterator() {
        return new IteratorHelper();
    }

    private class IteratorHelper implements Iterator<E> {
        private Node<E> tempNode;
        private long stateCheck;

        public IteratorHelper() {
            tempNode = head;
            stateCheck = modificationCounter;
        }
        public boolean hasNext() {
            if(stateCheck != modificationCounter) throw new ConcurrentModificationException();
            return (tempNode != null);
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
}//Eof
