package data_structures;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * William Fox: cssc0917
 * CS 310, Prog 1, ArrayLinearList
 */
public class ArrayLinearList<E> implements LinearListADT<E> {
    private E[] list;
    private int size;
    private int capacity;

    @SuppressWarnings("unchecked")
    public ArrayLinearList() {
        list = (E[]) new Object[DEFAULT_MAX_CAPACITY];
        capacity = DEFAULT_MAX_CAPACITY;
        size = 0;
    }

    @Override
    public void addLast(E obj) {
        insert(obj, size + 1);
    }

    @Override
    public void addFirst(E obj) {
        insert(obj, 1);
    }

    @Override
    public void insert(E obj, int location) {
        if (!isValidInsertLocation(location))
            throw new RuntimeException("Location does not map to a valid position within the list");
        if (isFull()) grow();
        upShift(location);
        list[location - 1] = obj;
        size++;
    }

    @Override
    public E remove(int location) {

        if (!isValidRemoveLocation(location))
            throw new RuntimeException("Location does not map to a valid position within the list");

        E temp = list[location - 1];
        downShift(location);
        size--;
        shrink(size);
        return temp;
    }

    @Override
    public E remove(E obj) {
        int location = locate(obj); //Saves location when found
        if (location == -1)         //List doesn't contain object, see locate(E obj) in interface
            return null;
        return remove(location);    //Uses found location to remove element
    }

    @Override
    public E removeFirst() {
        if (!isEmpty())
            return remove(1);
        return null;
    }

    @Override
    public E removeLast() {
        if (!isEmpty())
            return remove(size);
        return null;
    }

    @Override
    public E get(int location) {
        if (!isValidRemoveLocation(location))
            throw new RuntimeException("Location isn't a valid position in the list");

        return list[location - 1];
    }

    @SuppressWarnings("unchecked")
    @Override
    public boolean contains(E obj) {
        for (int i = 0; i < size; i++)
            if (((Comparable<E>) obj).compareTo(list[i]) == 0)
                return true;
        return false;
    }


    @SuppressWarnings("unchecked")
    @Override
    public int locate(E obj) {
        for (int i = 0; i < size; i++)
            if (((Comparable<E>) obj).compareTo(list[i]) == 0)
                return i + 1;
        return -1;
    }

    @Override
    public void clear() {
        size = 0;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public int size() {
        return size;
    }

    //My Helper Methods Are Bellow

    private boolean isFull() {
        return size == capacity;
    }

    //Checks to see if location to be removed is valid in the list
    private boolean isValidRemoveLocation(int location) {
        return ((location >= 1) && (location <= size));
    }

    //Checks to see if location to be inserted is valid in the list
    private boolean isValidInsertLocation(int location) {
        return ((location >= 1) && (location - 1 <= size));
    }

    //Grows list to twice current size
    @SuppressWarnings("unchecked")
    private void grow() {
        capacity *= 2;
        E[] temp = (E[]) new Object[capacity];
        for (int i = 0; i < size; i++) {
            temp[i] = list[i];
        }
        list = temp;
    }

    //Shrinks list to half size if necessary
    //Gets size from call to compensate for size-- for remove functions
    @SuppressWarnings("unchecked")
    private void shrink(int size) {
        if (size * 4 >= capacity)
            return; //Dosen't need to shrink, do nothing
        capacity /= 2;
        E[] temp = (E[]) new Object[capacity];
        for (int i = 0; i < size; i++) {
            temp[i] = list[i];
        }
        list = temp;
    }

    //Shifts all elements above location up by one index
    private void upShift(int location) {
        for (int i = size; i >= location; i--) {
            list[i] = list[i - 1];
        }
    }

    //Shifts all elements above location down by one index
    private void downShift(int location) {
        for (int i = location - 1; i < size - 1; i++) {
            list[i] = list[i + 1];
        }
    }


    @Override
    public Iterator<E> iterator() {
        return new IteratorHelper();
    }

    private class IteratorHelper implements Iterator<E> {
        private int iterIndex;

        public IteratorHelper() {
            iterIndex = 0;
        }

        @Override
        public boolean hasNext() {
            return iterIndex < size;
        }

        @SuppressWarnings("unchecked")
        @Override
        public E next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            return (E) list[iterIndex++];
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException();
        }
    }
}//Eof
